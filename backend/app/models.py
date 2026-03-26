from sqlalchemy import Column, Integer, Float, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# =====================================================
# PATIENT TABLE
# =====================================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="patient")


# =====================================================
# ASSESSMENT TABLE
# (Each time user runs prediction = new assessment)
# =====================================================
class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="assessments")
    features = relationship("MedicalFeatures", back_populates="assessment")
    predictions = relationship("Prediction", back_populates="assessment")


# =====================================================
# STORE ALL INPUT FEATURES
# =====================================================
class MedicalFeatures(Base):
    __tablename__ = "medical_features"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))

    # Store full input as JSON for flexibility
    raw_input = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="features")


# =====================================================
# PREDICTION TABLE
# =====================================================
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))

    disease = Column(String)
    confidence = Column(Float)
    risk_level = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="predictions")