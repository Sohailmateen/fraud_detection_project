# Loads data, trains & saves model

# src/train.py
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from database import get_training_data

# 1. Fetch engineered data from Postgres
df = get_training_data()

X = df[['amount', 'shipping_billing_match', 'account_age_days', 'risk_score']]
y = df['is_fraud']

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train Model (Handling imbalance using class_weight)
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate (Focusing on Recall/F1-score for fraud)
preds = model.predict(X_test)
print(classification_report(y_test, preds))

# 5. Save the trained model artifact
joblib.dump(model, '../models/fraud_model.pkl')
print("Model saved successfully!")


