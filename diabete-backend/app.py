from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os
import psycopg2
import redis
import json
from fastapi.middleware.cors import CORSMiddleware

# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ["*"] pour tout autoriser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Charger le modèle ML
# =========================
model = joblib.load("model/diabetes_model.pkl")

# =========================
# Connexion PostgreSQL
# =========================
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    pregnancies FLOAT,
    glucose FLOAT,
    bloodpressure FLOAT,
    skinthickness FLOAT,
    insulin FLOAT,
    bmi FLOAT,
    dpf FLOAT,
    age FLOAT,
    prediction INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# =========================
# Connexion Redis
# =========================
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# =========================
# Pydantic model
# =========================
class DiabetesInput(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

# =========================
# Healthcheck
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# Endpoint /predict avec cache Redis + PostgreSQL
# =========================
@app.post("/predict")
def predict(data: DiabetesInput):

    cache_key = json.dumps(data.dict(), sort_keys=True)

    # 1️⃣ Vérifier le cache
    cached_prediction = redis_client.get(cache_key)
    if cached_prediction:
        return {
            "prediction": int(cached_prediction),
            "source": "cache"
        }

    # 2️⃣ Calcul ML
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)

    # 3️⃣ Stocker en cache (TTL 1h)
    redis_client.setex(cache_key, 3600, int(prediction[0]))

    # 4️⃣ Stocker en base PostgreSQL
    cursor.execute("""
    INSERT INTO predictions (
        pregnancies, glucose, bloodpressure,
        skinthickness, insulin, bmi, dpf, age, prediction
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.Pregnancies,
        data.Glucose,
        data.BloodPressure,
        data.SkinThickness,
        data.Insulin,
        data.BMI,
        data.DiabetesPedigreeFunction,
        data.Age,
        int(prediction[0])
    ))
    conn.commit()

    return {
        "prediction": int(prediction[0]),
        "source": "model"
    }
