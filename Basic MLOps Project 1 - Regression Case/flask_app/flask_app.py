import pickle
import numpy as np
import pandas as pd
import os
from flask import Flask, request, app, jsonify, url_for, render_template

current_dir = os.getcwd()
root_dir = os.path.dirname(current_dir)
model_folder = os.path.join(root_dir, "models")
template_folder = os.path.join(root_dir, "templates")
os.makedirs(model_folder, exist_ok=True)

app=Flask(__name__, template_folder=template_folder)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load california housing regression model pickle 
model_filename = os.path.join(model_folder, "california_housing_linear_regression_model.pkl")
with open(model_filename, "rb") as file:
    reg_model = pickle.load(file)

# LOad standard scaler pickle 
model_filename = os.path.join(model_folder, "standard_scaler.pkl")
with open(model_filename, "rb") as file:
    scaler = pickle.load(file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    data_reshape = np.array(list(data.values())).reshape(1,-1)
    print(data_reshape)
    data_scaled = scaler.transform(data_reshape)
    prediction = reg_model.predict(data_scaled)
    print(prediction[0])
    return jsonify(prediction[0])

@app.route('/predict', methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scaler.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=reg_model.predict(final_input)[0]
    output_dollar=output*100000
    formatted_number = format(output_dollar, ",.2f")
    return render_template("home.html", prediction_text=f"The estimated house price for the given parameters is ${formatted_number}")

if __name__=="__main__":
    app.run(debug=True)
    