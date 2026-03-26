import numpy as np
import joblib
import os

# Go to backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to backend/models/heart_model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "models", "heart_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_disease(data):
    input_data = np.array([[
        data.age,
        data.sex,
        data.cp,
        data.trestbps,
        data.chol,
        data.fbs,
        data.restecg,
        data.thalach,
        data.exang,
        data.oldpeak,
        data.slope,
        data.ca,
        data.thal
    ]])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
            return "High Risk of Heart Disease"
    else:
            return "Low Risk of Heart Disease"
    return str(prediction[0])