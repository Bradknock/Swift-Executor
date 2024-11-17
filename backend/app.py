from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./data.json"))

# Specify the directory to save uploaded files
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_pipe():
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    return data["pipes"]

@app.route('/api/pipes', methods=['GET'])
def get_pipes():
    return jsonify(load_pipe())

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    user_input = data.get('input')
    return jsonify({"output": user_input})
  
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"message": "No file part"}, 400

    file = request.files['file']

    if file.filename == '':
        return {"message": "No selected file"}, 400

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return {"message": "File successfully uploaded"}, 200
    else:
        return {"message": "Invalid file type. Only CSV files are allowed."}, 400


if __name__ == '__main__':
    app.run(debug=True)