# data/populate_data.py
import random
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:8867196614@localhost:5432/fraud_db")

def populate():
    with engine.begin() as conn:
        # Clear old testing data
        conn.execute(text("TRUNCATE transactions CASCADE; TRUNCATE users CASCADE;"))
        
        print("Generating 1,000 mock records...")
        for i in range(1, 1001):
            # 1. Generate User
            account_age = random.randint(1, 730) # up to 2 years
            risk_score = round(random.uniform(0.0, 1.0), 2)
            conn.execute(
                text("INSERT INTO users (user_id, account_age_days, risk_score) VALUES (:uid, :age, :risk)"),
                {"uid": i, "age": account_age, "risk": risk_score}
            )
            
            # 2. Generate Transaction (Imbalanced: ~10% Fraud)
            amount = round(random.uniform(5.0, 2000.0), 2)
            shipping_match = random.choice([1, 1, 1, 0]) # mostly matching
            
            # Make logic realistic: High amounts + mismatch = likely fraud
            if amount > 1200 and shipping_match == 0 or risk_score > 0.85:
                is_fraud = random.choice([1, 1, 0]) # Higher chance of fraud
            else:
                is_fraud = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) # 10% chance
                
            conn.execute(
                text("""INSERT INTO transactions (user_id, amount, shipping_billing_match, is_fraud) 
                        VALUES (:uid, :amt, :match, :fraud)"""),
                {"uid": i, "amt": amount, "match": shipping_match, "fraud": is_fraud}
            )
    print("Database successfully populated!")

if __name__ == "__main__":
    populate()
