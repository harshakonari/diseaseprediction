# predict_engine.py

import joblib
import os
import numpy as np

# Base directory (backend folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Models folder path
MODEL_DIR = os.path.join(BASE_DIR, "models")

heart_model = joblib.load(os.path.join(MODEL_DIR, "heart_model.pkl"))
heart_scaler = joblib.load(os.path.join(MODEL_DIR, "heart_scaler.pkl"))

diabetes_model = joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl"))
diabetes_scaler = joblib.load(os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))

liver_model = joblib.load(os.path.join(MODEL_DIR, "liver_model.pkl"))
liver_scaler = joblib.load(os.path.join(MODEL_DIR, "liver_scaler.pkl"))

# ---------------------------
# Risk Level Function
# ---------------------------
def get_risk_level(prob):
    if prob < 0.3:
        return "Low"
    elif prob < 0.7:
        return "Medium"
    else:
        return "High"


# ---------------------------
# Heart Prediction
# ---------------------------
def predict_heart(data: list):
    scaled = heart_scaler.transform([data])
    prob = heart_model.predict_proba(scaled)[0][1]
    risk = get_risk_level(prob)

    return {
        "disease": "Heart Disease",
        "risk_level": risk,
        "confidence": round(float(prob) * 100, 2),
        "recommendation": heart_recommendation(risk)
    }


def heart_recommendation(risk):
    if risk == "High":
        return "Consult a cardiologist immediately."
    elif risk == "Medium":
        return "Monitor cholesterol and blood pressure regularly."
    else:
        return "Maintain healthy lifestyle and regular exercise."


# ---------------------------
# Diabetes Prediction
# ---------------------------
def predict_diabetes(data: list):
    scaled = diabetes_scaler.transform([data])
    prob = diabetes_model.predict_proba(scaled)[0][1]
    risk = get_risk_level(prob)

    return {
        "disease": "Diabetes",
        "risk_level": risk,
        "confidence": round(float(prob) * 100, 2),
        "recommendation": diabetes_recommendation(risk)
    }


def diabetes_recommendation(risk):
    if risk == "High":
        return "Consult endocrinologist and check HbA1c immediately."
    elif risk == "Medium":
        return "Control sugar intake and monitor glucose weekly."
    else:
        return "Maintain balanced diet and active lifestyle."


# ---------------------------
# Liver Prediction
# ---------------------------
def predict_liver(data: list):
    scaled = liver_scaler.transform([data])
    prob = liver_model.predict_proba(scaled)[0][1]
    risk = get_risk_level(prob)

    return {
        "disease": "Liver Disease",
        "risk_level": risk,
        "confidence": round(float(prob) * 100, 2),
        "recommendation": liver_recommendation(risk)
    }


def liver_recommendation(risk):
    if risk == "High":
        return "Consult hepatologist and perform liver function tests."
    elif risk == "Medium":
        return "Avoid alcohol and monitor liver enzymes."
    else:
        return "Maintain healthy diet and hydration."
    

# ---------------------------
# UNIFIED MULTI-DISEASE PREDICTOR
# ---------------------------

def predict_all(patient_data: dict):

    results = []

    # HEART INPUT ORDER (must match training order)
    heart_input = [
        patient_data["age"],
        patient_data["sex"],
        patient_data["cp"],
        patient_data["trestbps"],
        patient_data["chol"],
        patient_data["fbs"],
        patient_data["restecg"],
        patient_data["thalach"],
        patient_data["exang"],
        patient_data["oldpeak"],
        patient_data["slope"],
        patient_data["ca"],
        patient_data["thal"]
    ]

    heart_result = predict_heart(heart_input)
    results.append(heart_result)


    # DIABETES INPUT ORDER
    diabetes_input = [
        patient_data["pregnancies"],
        patient_data["glucose"],
        patient_data["bloodpressure"],
        patient_data["skinthickness"],
        patient_data["insulin"],
        patient_data["bmi"],
        patient_data["dpf"],
        patient_data["age"]
    ]

    diabetes_result = predict_diabetes(diabetes_input)
    results.append(diabetes_result)


    # LIVER INPUT ORDER
    liver_input = [
        patient_data["age"],
        patient_data["gender"],
        patient_data["total_bilirubin"],
        patient_data["direct_bilirubin"],
        patient_data["alkaline_phosphotase"],
        patient_data["alamine_aminotransferase"],
        patient_data["aspartate_aminotransferase"],
        patient_data["total_proteins"],
        patient_data["albumin"],
        patient_data["albumin_globulin_ratio"]
    ]

    liver_result = predict_liver(liver_input)
    results.append(liver_result)


    # Sort by confidence descending
    results = sorted(results, key=lambda x: x["confidence"], reverse=True)

    return results