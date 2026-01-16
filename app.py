from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model and columns
model = joblib.load("car_price_model.pkl")
model_columns = joblib.load("model_columns.pkl")

@app.route('/')
def home():
    return render_template('index.html')  # HTML file we'll create

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    
    # Convert numeric fields
    data['Year'] = int(data['Year'])
    data['Mileage'] = int(data['Mileage'])
    
    # Prepare input dataframe with zeros
    input_df = pd.DataFrame([[0]*len(model_columns)], columns=model_columns)
    
    # Fill numeric values
    input_df['Year'] = data['Year']
    input_df['Mileage'] = data['Mileage']
    
    # Fill categorical values
    for col in model_columns:
        if col in data and int(data[col]) == 1:
            input_df[col] = 1

    # Predict
    prediction = model.predict(input_df)[0]
    
    return render_template('index.html', prediction_text=f"Estimated Price: {int(prediction)} PKR")

if __name__ == '__main__':
    app.run(debug=True)
