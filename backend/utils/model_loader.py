import joblib
from pathlib import Path

MODEL_PATH = Path("models/diabetes_model.pkl")

def load_model():
    return joblib.load(MODEL_PATH)
