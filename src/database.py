# Handles Postgres connection  

# src/database.py
import pandas as pd
from sqlalchemy import create_engine

def get_training_data():
    # Create an engine using standard database string URI
    # Format: postgresql://username:password@host:port/database_name
    engine = create_engine("postgresql://postgres:8867196614@localhost:5432/fraud_db")
    
    query = """
        SELECT t.amount, t.shipping_billing_match, u.account_age_days, u.risk_score, t.is_fraud
        FROM transactions t
        JOIN users u ON t.user_id = u.user_id;
    """
    
    # Read data cleanly using the engine
    df = pd.read_sql_query(query, engine)
    return df
