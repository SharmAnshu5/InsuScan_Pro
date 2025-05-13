# main.py (FastAPI backend)
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import joblib
import pandas as pd
import numpy as np  # Add numpy import
import logging
import traceback
import os
from typing import Dict, Any, Optional
from utils.extract_diabetes_data import extract_text_from_file, extract_diabetes_features
from utils.summary_generator import generate_summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("insu-scan-api")

# Initialize FastAPI app
app = FastAPI(title="Insu Scan Pro API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load model
try:
    model_path = "models/diabetes_model.pkl"
    if not os.path.exists(model_path):
        logger.warning(f"Model file {model_path} not found!")
    model = joblib.load(model_path)
    logger.info("Diabetes model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    model = None

# Define model features
model_features = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

# Error handler middleware
@app.middleware("http")
async def exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/process_report/")
async def process_report(file: UploadFile = File(...)):
    """
    Process an uploaded medical report file
    
    Args:
        file: The uploaded file (PDF, DOCX, or TXT)
        
    Returns:
        Extracted values, prediction, and summary
    """
    logger.info(f"Processing report: {file.filename}")
    
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file type. Please upload PDF, DOCX, or TXT file."}
            )
        
        # Read file contents
        contents = await file.read()
        if not contents:
            return JSONResponse(
                status_code=400,
                content={"error": "Empty file uploaded"}
            )
        
        # Extract text from file
        text = extract_text_from_file(file.filename, contents)
        
        # Check if text extraction was successful
        if text.startswith("Error") or text.startswith("Unsupported"):
            logger.error(f"Text extraction failed: {text}")
            return JSONResponse(
                status_code=422,
                content={"error": text}
            )
        
        # Extract features from text
        values = extract_diabetes_features(text)
        logger.info(f"Extracted features: {values}")
        
        # Prepare data for model prediction - ensure all values are Python native types
        model_input = {}
        for key in model_features:
            try:
                # Convert any potential numpy types to Python native types
                value = values.get(key, 0)
                if hasattr(value, "item"):  # Check if it's a numpy scalar
                    value = value.item()  # Convert numpy scalar to Python native type
                model_input[key] = float(value)
            except (ValueError, TypeError) as e:
                logger.warning(f"Error converting {key}: {str(e)}")
                model_input[key] = 0.0
        
        # Make prediction if model is available
        if model is not None:
            df = pd.DataFrame([model_input])
            prob = model.predict_proba(df)[0][1]
            
            # Convert numpy float to Python float
            if isinstance(prob, np.floating):
                prob = float(prob)
                
            prediction = int(prob > 0.5)
            
            # Determine diabetes type based on age
            age = values.get("Age", 0)
            try:
                age = float(age)
                diabetes_type = "Type 2" if age > 25 else "Type 1"
            except (ValueError, TypeError):
                diabetes_type = "Type 2"  # Default
                
            # Generate summary
            summary = generate_summary(values, prediction, prob * 100, diabetes_type)
            
            return {
                "extracted_values": values,
                "prediction": "Diabetes" if prediction else "No Diabetes",
                "confidence": prob * 100,
                "diabetes_type": diabetes_type,
                "summary": summary
            }
        else:
            # If model isn't available, just return extracted values
            logger.warning("Model not available, returning only extracted values")
            return {
                "extracted_values": values,
                "prediction": "Model unavailable",
                "confidence": 0,
                "diabetes_type": "Unknown",
                "summary": "Prediction model is currently unavailable."
            }
            
    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )

@app.post("/predict/")
async def predict_diabetes(request: Dict[str, Any]):
    """
    Make diabetes prediction from manually entered data
    
    Args:
        request: Dictionary containing patient data
        
    Returns:
        Prediction result and summary
    """
    try:
        if "data" not in request:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing 'data' field in request"}
            )
            
        data = request["data"]
        
        # Validate data
        if not isinstance(data, dict):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid data format. Expected dictionary."}
            )
        
        # Ensure all required model features are present
        model_input = {}
        for key in model_features:
            try:
                value = data.get(key, 0)
                if hasattr(value, "item"):  # Check if it's a numpy scalar
                    value = value.item()  # Convert numpy scalar to Python native type
                model_input[key] = float(value)
            except (ValueError, TypeError):
                model_input[key] = 0.0
        
        # Make prediction if model is available
        if model is not None:
            df = pd.DataFrame([model_input])
            prob = model.predict_proba(df)[0][1]
            
            # Convert numpy float to Python float
            if isinstance(prob, np.floating):
                prob = float(prob)
                
            prediction = int(prob > 0.5)
            
            # Determine diabetes type
            age = data.get("Age", 0)
            try:
                age = float(age)
                diabetes_type = "Type 2" if age > 25 else "Type 1"
            except (ValueError, TypeError):
                diabetes_type = "Type 2"  # Default
            
            # Generate summary
            summary = generate_summary(data, prediction, prob * 100, diabetes_type)
            
            return {
                "prediction": "Diabetes" if prediction else "No Diabetes",
                "confidence": prob * 100,
                "diabetes_type": diabetes_type,
                "summary": summary
            }
        else:
            return JSONResponse(
                status_code=503,
                content={"error": "Prediction model is not available"}
            )
            
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction failed: {str(e)}"}
        )

# Run with: uvicorn main:app --reload