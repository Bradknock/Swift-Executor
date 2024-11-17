from flask import request, jsonify, render_template
from datetime import datetime
import numpy as np
from app import flask_app, db
import pickle
from models import rawdata

# Load your ML model
model = pickle.load(open("model.pkl", "rb"))

@flask_app.route("/")
def home():
    return render_template("index.html")

@flask_app.route("/get", methods=["GET"])
def get_rawdata():
    pipe_data=rawdata.querry.all()
    result=[data.to_json() for data in pipe_data]
    return jsonify(result)
@flask_app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract form data
        gas_set = float(request.form.get("inj_setpt"))
        gas_instant = float(request.form.get("inj_act"))
        pipe_name = request.form.get("inj_name")
        valve_perc = float(request.form.get("inj_perc"))
        time = datetime.strptime(request.form.get("inj_time"), "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    # Prepare features for prediction
    features = np.array([[gas_set, gas_instant]])
    prediction = model.predict(features)
    prediction_value = int(prediction[0])

    # Store the data in the database
    new_data = rawdata(
        name=pipe_name,
        time=time,
        inj_act=gas_instant,
        inj_setpt=gas_set,
        inj_perc=valve_perc,
        time_until_hyd=3600000
    )
    db.session.add(new_data)
    db.session.commit()

    return render_template("index.html", prediction_text=f"Has hydration occurred? {prediction[0]}")
