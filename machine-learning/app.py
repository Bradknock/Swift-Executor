import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():

    gas_set = float(request.form.get("inj_setpt"))
    gas_instant = float(request.form.get("inj_act"))
   

    
    #float_features = [float(x) for x in request.form.values()]
    features = np.array([[gas_set, gas_instant]])

    prediction = model.predict(features)
    return render_template("index.html", prediction_text = "Has hydration occurred?  {}".format(prediction))

if __name__ == "__main__":
    flask_app.run(debug=True)