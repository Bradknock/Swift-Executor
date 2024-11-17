import os
import json
import requests
import pickle
import pandas as pd

def send_each(src_path, route="http://localhost:5000/api/pipes"): #r0
    for each in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, each)):
            send_each(os.path.join(src_path, each))
        else:
            with open(os.path.join(src_path, each), "r") as f:
                data = json.load(f)
            r = requests.post(route, json=data)
            print(r.text)
            

def analyze_data(csv_src_path, model_pkl_path):
    with open(model_pkl_path, "rb") as f:
        print("it ran")
        model = pickle.load(f)
        
    
    # Open the CSV file and save as pandas dataframe
    df = pd.read_csv(csv_src_path)
    
    # Predict the target column using the model
    df["prediction"] = model.predict(df)
    
    # Save the dataframe as a new CSV file
    df.to_csv("prediction.csv", index=False)
    
    # send the prediction.csv to the server
    send_each("prediction.csv", route="http://localhost:5000/api/echo") # r1