
# End-to-End Enterprise Fraud Detection Pipeline

A production-ready Machine Learning engineering pipeline designed to predict transaction fraud using real-time database queries and a high-performance REST API wrapper.

This project demonstrates the transition from raw transactional database data to a deployed, scalable inference endpoint, shifting away from isolated Jupyter Notebook workflows into modular software engineering principles.

## 🚀 System Architecture & Workflow

1. **Data Infrastructure Layer:** Transaction and user profile datasets are structurally organized and maintained inside a relational **PostgreSQL** instance.
2. **Feature Engineering & Extract (ETL):** Optimized SQL relational `JOIN` queries fetch operational features directly into Python, bypassing flat CSV dependencies.
3. **Model Engineering Stack:** A robust **Random Forest Classifier** is trained using `scikit-learn`, integrating class-balancing algorithms to handle high data skewness (~10% fraud distribution).
4. **Production API Endpoint:** The serialized model artifact is integrated with **FastAPI**, serving live low-latency JSON predictions via a `/predict` payload validation layer (`Pydantic`).

---

## 📁 Repository Structure

```text
fraud_detection_project/
│
├── data/
│   └── populate_data.py       # Programmatic PostgreSQL data generation matrix
│
├── src/
│   ├── database.py            # Optimized SQLAlchemy transactional connector
│   ├── train.py               # Model training, evaluation matrix, and serialization
│   └── predict.py             # Live FastAPI application routing & prediction schemas
│
├── models/
│   └── fraud_model.pkl        # Production model binary (Serialized artifact)
│
├── requirements.txt           # Explicit version-locked project dependencies
└── README.md                  # System engineering documentation
```

---

## 🛠️ Performance & Evaluation Metrics

The model evaluation strategy focuses strictly on **Recall** and **F1-Score** for the minor class (`1`) to prevent uncaught fraudulent exposure:

```text
              precision    recall  f1-score   support

           0       0.89      0.87      0.88       150
           1       0.64      0.68      0.66        50

    accuracy                           0.82       200
```

* **Fraud Recall (0.68):** Successfully catches 68% of all true system fraud cases.
* **Class Balancing:** Effectively mitigates extreme data imbalance without synthetic oversampling downfalls.

---

## 💻 Technical Execution & Setup

### 1. Environment Isolation

Clone the repository and spin up an isolated virtual environment to prevent dependency collisions:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Dependency Resolution

Install all performance-critical libraries from the locked requirements map:

```bash
pip install -r requirements.txt
```

### 3. Pipeline Operation

Initialize the local database generation script and trigger the machine learning training runtime:

```bash
python data/populate_data.py
python src/train.py
```

### 4. Deploying the Live Inference Engine

Fire up the local development ASGI web server using Uvicorn:

```bash
uvicorn src.predict:app --reload
```

Navigate to `http://127.0.0` to access the interactive OpenAPI/Swagger user interface.

---

## 🔌 API Contract Reference

### Base URL Route (`GET /`)

Confirms API system health and structural connectivity.

### Inference Gateway (`POST /predict`)

**Sample Input Payload Structure:**

```json
{
  "amount": 1850.00,
  "shipping_billing_match": 0,
  "account_age_days": 2,
  "risk_score": 0.91
}
```

**Sample Output Prediction Matrix:**

```json
{
  "is_fraud": 1,
  "fraud_probability": 0.61,
  "status": "High Risk"
}
```
