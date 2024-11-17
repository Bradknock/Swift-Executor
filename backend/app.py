from flask import Flask, json
from flask_cors import CORS
from extensions import db
from flask import request, jsonify, render_template
from datetime import datetime
import numpy as np
from models import rawdata
import pickle
from flask_migrate import Migrate

# Initialize Flask app
flask_app = Flask(__name__)
CORS(flask_app)

# Database configuration
flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rawdata.db"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the app context
db.init_app(flask_app)

migrate=Migrate(flask_app, db)

# Create the database tables if they don't exist
with flask_app.app_context():
    db.create_all()


model_95 = pickle.load(open("model_95.pkl", "rb"))

@flask_app.route("/")
def home():
    return render_template("index.html")

@flask_app.route("/view", methods=["GET"])
def get_rawdata():
    pipe_data=rawdata.query.all()
    result=[data.to_json() for data in pipe_data]
    return jsonify(result)

@flask_app.route("/delete", methods=["DELETE"])
def delete_data():
    try:
        # Delete all records from the RawData table
        db.session.query(rawdata).delete()
        db.session.commit()
        return jsonify({"message": "Data deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback if any error occurs
        return jsonify({"error": str(e)}), 500
    


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
    featuresx = np.array([[gas_set, gas_instant]])

    predictionx = model_95.predict(featuresx)
    prediction_valuex = int(predictionx[0])


    # Store the data in the database
    new_data = rawdata(
        name=pipe_name,
        time=time,
        inj_act=gas_instant,
        inj_setpt=gas_set,
        inj_perc=valve_perc,
        hyd_status=prediction_valuex,
        time_until_hyd=3600000,
    )
    db.session.add(new_data)
    db.session.commit()

    return render_template("index.html", prediction_text=f"Has hydration occurred? {(prediction_valuex)}")

@flask_app.route("/get_prediction", methods=["GET"])
def get_latest_prediction():
    # Fetch the latest prediction value from the database
    latest_data = rawdata.query.filter_by(name='pipe5').order_by(rawdata.time.desc()).first()
    if latest_data:
        return jsonify({"prediction_value": latest_data.hyd_status, "prediction_name": latest_data.name})
    else:
        return jsonify({"error": "No data found"}), 404
    


if __name__ == "__main__":
    flask_app.run(debug=True)
