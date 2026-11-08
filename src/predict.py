# FastAPI application code 

# src/predict.py
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Initialize the FastAPI application
app = FastAPI(title="Fraud Detection API", version="1.0")

# 2. Load the trained model into memory
model = joblib.load('../models/fraud_model.pkl')

# 3. Define the data structure the API expects to receive
class TransactionInput(BaseModel):
    amount: float
    shipping_billing_match: int
    account_age_days: int
    risk_score: float
    
# 4. route page
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Production Fraud Detection API",
        "status": "Healthy",
        "documentation_url": "http://127.0.0"
    }


# 5. Create the prediction endpoint
import pandas as pd  # Make sure to import pandas at the top

@app.post("/predict")
def predict_fraud(data: TransactionInput):
    # Convert incoming JSON data into a structured Pandas DataFrame with matching column names
    input_df = pd.DataFrame([{
        "amount": data.amount,
        "shipping_billing_match": data.shipping_billing_match,
        "account_age_days": data.account_age_days,
        "risk_score": data.risk_score
    }])
    
    # Run prediction safely using the DataFrame
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)
    
    return {
        "is_fraud": int(prediction[0]),
        "fraud_probability": float(probability[0][1]), # Grab the probability of being fraud (class 1)
        "status": "High Risk" if prediction[0] == 1 else "Safe Transaction"
    }

