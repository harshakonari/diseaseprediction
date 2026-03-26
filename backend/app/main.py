from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from .database import SessionLocal, engine
from . import models
from predict_engine import predict_all
from fastapi.middleware.cors import CORSMiddleware
import json

models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend-name.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# UNIFIED PATIENT INPUT MODEL
# -----------------------------
class PatientData(BaseModel):

    # -------- HEART --------
    age: int
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

    # -------- DIABETES --------
    pregnancies: int
    glucose: float
    bloodpressure: float
    skinthickness: float
    insulin: float
    bmi: float
    dpf: float

    # -------- LIVER --------
    gender: int
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    alamine_aminotransferase: float
    aspartate_aminotransferase: float
    total_proteins: float
    albumin: float
    albumin_globulin_ratio: float


# -----------------------------
# UNIFIED PREDICT ENDPOINT
# -----------------------------
@app.post("/predict")
def predict(data: PatientData, db: Session = Depends(get_db)):

    # Convert to dictionary
    input_data = data.dict()

    # Run all ML models
    results = predict_all(input_data)

    # Get top prediction
    top_result = max(results, key=lambda x: x["confidence"])

    # ------------------------------
    # SAVE PATIENT BASIC INFO FIRST
    # ------------------------------
    # Try to find existing patient
    patient = db.query(models.Patient).filter(
        models.Patient.age == data.age,
        models.Patient.gender == data.sex
    ).first()

    # If not found → create new
    if not patient:
        patient = models.Patient(
            age=data.age,
            gender=data.sex
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        

        db.add(patient)
        db.commit()
        db.refresh(patient)

    # ------------------------------
    # SAVE ASSESSMENT
    # ------------------------------
    assessment = models.Assessment(
        patient_id=patient.id
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # ------------------------------
    # SAVE FEATURES
    # ------------------------------
    features = models.MedicalFeatures(
    assessment_id=assessment.id,
    raw_input=input_data
    )

    db.add(features)
    db.commit()

    # ------------------------------
    # SAVE TOP PREDICTION
    # ------------------------------
    prediction_record = models.Prediction(
        assessment_id=assessment.id,
        disease=top_result["disease"],
        confidence=top_result["confidence"],
        risk_level=top_result["risk_level"]
    )

    db.add(prediction_record)
    db.commit()

    return {
        "status": "success",
        "top_prediction": top_result,
        "all_probable_diseases": results
    }
# -----------------------------
# BASIC ASSESSMENT MODEL
# -----------------------------
class BasicAssessment(BaseModel):
    age: int
    gender: str
    symptoms: list[str]


@app.post("/start-assessment")
def start_assessment(data: BasicAssessment):

    symptom_map = {
        "Heart Disease": ["chest pain", "shortness of breath", "fatigue","fever"],
        "Diabetes": ["frequent urination", "increased thirst", "fatigue"],
        "Liver Disease": ["yellow skin", "abdominal pain", "fatigue"]
    }

    disease_scores = {}

    for disease, symptom_list in symptom_map.items():
        score = len(set(data.symptoms).intersection(symptom_list))
        disease_scores[disease] = score

    sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

    probable = [d[0] for d in sorted_diseases if d[1] > 0]

    next_questions = []

    if probable:
        top_disease = probable[0]

        if top_disease == "Heart Disease":
            next_questions = [
                "What is your resting blood pressure?",
                "What is your cholesterol level?",
                "Do you have exercise-induced chest pain? (0/1)"
            ]

        elif top_disease == "Diabetes":
            next_questions = [
                "What is your fasting glucose level?",
                "What is your BMI?",
                "What is your insulin level?"
            ]

        elif top_disease == "Liver Disease":
            next_questions = [
                "What is your total bilirubin?",
                "What is your albumin level?",
                "Do you consume alcohol regularly? (0/1)"
            ]

    return {
        "probable_diseases": probable,
        "next_questions": next_questions
    }