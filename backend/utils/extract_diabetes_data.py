
from io import BytesIO
import fitz  # PyMuPDF
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import docx with proper error handling
try:
    from docx import Document
except ImportError:
    # Create a fallback function if python-docx is not installed
    def extract_text_from_docx(file_bytes):
        return "Error: python-docx library not installed. Cannot process DOCX files."
else:
    def extract_text_from_docx(file_bytes):
        try:
            doc = Document(BytesIO(file_bytes))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"DOCX extraction error: {str(e)}"

def extract_text_from_file(filename, file_bytes):
    """Extract text from various file formats with robust error handling"""
    try:
        if not filename or not file_bytes:
            return "Error: Invalid file or empty content"
            
        if filename.lower().endswith(".pdf"):
            return extract_text_from_pdf(file_bytes)
        elif filename.lower().endswith(".docx"):
            return extract_text_from_docx(file_bytes)
        elif filename.lower().endswith(".txt"):
            # Handle possible encoding issues
            try:
                return file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    return file_bytes.decode("latin-1")
                except Exception:
                    return "Error: Unable to decode text file with supported encodings"
        else:
            return f"Unsupported file type: {filename}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF with improved error handling and OCR fallback option"""
    text = ""
    try:
        # Convert bytes to BytesIO for safer handling
        file_stream = BytesIO(file_bytes)
        with fitz.open(stream=file_stream, filetype="pdf") as doc:
            # Get total pages for logging
            total_pages = len(doc)
            logger.info(f"Processing PDF with {total_pages} pages")
            
            # Process each page
            for page_num in range(total_pages):
                try:
                    page = doc[page_num]
                    page_text = page.get_text()
                    
                    # Log if page has very little text (might be an image-only page)
                    if len(page_text.strip()) < 50:
                        logger.warning(f"Page {page_num+1} has little text, might be image-based")
                    
                    text += page_text
                except Exception as e:
                    text += f"\n[Error extracting page {page_num}: {str(e)}]\n"
        
        if not text.strip():
            return "Error: No text content extracted from PDF. The PDF might be image-based and require OCR."
        return text
    except Exception as e:
        return f"PDF extraction error: {str(e)}"

def extract_diabetes_features(text):
    """Extract diabetes features from text using enhanced regex patterns"""
    features = {
        "PatientName": "N/A",
        "Gender": "N/A",
        "DoctorNotes": "Not provided",
        "DietRecommendation": "Not specified",
        "Pregnancies": 0,
        "Glucose": 0,
        "BloodPressure": 0,
        "SkinThickness": 0,
        "Insulin": 0,
        "BMI": 0.0,
        "DiabetesPedigreeFunction": 0.0,
        "Age": 0
    }
    
    # Enhanced dictionary of regex patterns for each field
    patterns = {
        # Enhanced patterns with more variations
        "PatientName": r"(?:Patient\s*Name|Name\s*of\s*Patient Name)[\s:]*[:\-=]?\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+)(?:\s*\n|\s*,|\s*\(|$)",
        
        "Gender": r"(?:Gender|Sex|Patient\s*Gender|Patient\s*Sex)[\s:]*[:\-=]?\s*(Male|Female|M|F|Other|male|female|m|f)(?:\s*\n|\s*,|$)",
        
        "Age": r"(?:Age|Years|Patient\s*Age|Age\s*\(years\)|Years\s*Old)[\s:]*[:\-=]?\s*(\d+)(?:\s*\n|\s*,|\s*years|\s*yrs|$)",
        
        "Pregnancies": r"(?:Pregnancies|Number\s*of\s*Pregnancies|Pregnancy\s*Count|No\.\s*of\s*Pregnancies)[\s:]*[:\-=]?\s*(\d+)(?:\s*\n|\s*,|$)",
        
        "Glucose": r"(?:Glucose|Blood\s*Glucose|Plasma\s*Glucose|Fasting\s*(?:Blood\s*)?Glucose|FBS|Random\s*(?:Blood\s*)?Glucose|RBS|Glucose\s*Level)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|\s*mg|\s*mmol|$)",
        
        "BloodPressure": r"(?:Blood\s*Pressure|BP|Diastolic\s*BP|Systolic\s*BP|Diastolic|Systolic)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|\s*mm|\s*Hg|$)",
        
        "SkinThickness": r"(?:Skin\s*Thickness|Triceps\s*Skin\s*Thickness|Triceps\s*Thickness|Skin\s*Fold)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|\s*mm|$)",
        
        "Insulin": r"(?:Insulin|Serum\s*Insulin|Insulin\s*Level|Fasting\s*Insulin\s*Dose|Insulin\s*Dose)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|\s*(?:μU|mU|IU)?(?:/ml)?|$)",
        
        "BMI": r"(?:BMI|Body\s*Mass\s*Index|Mass\s*Index)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|\s*kg|$)",
        
        "DiabetesPedigreeFunction": r"(?:Diabetes\s*Pedigree\s*Function|Family\s*History|DPF|Pedigree\s*Function|Pedigree\s*Score|Family\s*History\s*Score)[\s:]*[:\-=]?\s*(\d+(?:\.\d+)?)(?:\s*\n|\s*,|$)",
        
        "DoctorNotes": r"(?:Doctor'?s?\s*Notes|Physician'?s?\s*Notes|Medical\s*Notes|Notes|Comments|Observations|Clinical\s*Notes)[\s:]*[:\-=]?\s*([\s\S]*?)(?=\n\s*\n|\Z)",
        
        "DietRecommendation": r"(?:Diet\s*Recommendation|Diet\s*Advice|Dietary\s*Guidelines|Nutrition\s*Advice|Dietary\s*Recommendations|Diet\s*Plan|Nutritional\s*Guidelines)[\s:]*[:\-=]?\s*([\s\S]*?)(?=\n\s*\n|\Z)"
    }
    
    # Extract each feature using the patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Convert numeric values
            if key not in ["PatientName", "Gender", "DoctorNotes", "DietRecommendation"]:
                try:
                    features[key] = float(value)
                except ValueError:
                    # Try to extract numeric value if mixed with text
                    numeric_match = re.search(r'(\d+(?:\.\d+)?)', value)
                    if numeric_match:
                        try:
                            features[key] = float(numeric_match.group(1))
                        except ValueError:
                            pass  # Keep default if conversion fails
            else:
                features[key] = value
    
    # Log extraction results
    logger.info(f"Data extraction complete. Found {sum(1 for v in features.values() if v not in ['N/A', 'Not provided', 'Not specified', 0, 0.0])} fields")
    
    return features