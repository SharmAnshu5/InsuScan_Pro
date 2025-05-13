import streamlit as st
import requests
import altair as alt
import json
import os
import time
from PIL import Image
import io

# Configuration
st.set_page_config(page_title="Insu Scan Pro", page_icon="💉", layout="wide")

# Constants
EXTRACTION_URL = "http://localhost:8000/process_report/"
PREDICTION_URL = "http://localhost:8000/predict/"
HEALTH_CHECK_URL = "http://localhost:8000/health"

# Initialize session state variables
if "extracted_values" not in st.session_state:
    st.session_state.extracted_values = {
        "PatientName": "N/A",
        "Gender": "N/A",
        "Age": 0,
        "DoctorNotes": "Not provided",
        "DietRecommendation": "Not specified",
        "Pregnancies": 0,
        "Glucose": 0,
        "Insulin": 0,
        "BloodPressure": 0,
        "SkinThickness": 0,
        "BMI": 0.0,
        "DiabetesPedigreeFunction": 0.0
    }

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = {
        "prediction": "No Prediction",
        "confidence": 0.0,
        "diabetes_type": "Unknown",
        "summary": "Please upload a report and extract data to generate a summary."
    }

if "file_content" not in st.session_state:
    st.session_state.file_content = None

if "page_number" not in st.session_state:
    st.session_state.page_number = 0

if "api_status" not in st.session_state:
    st.session_state.api_status = "Unknown"

# Check API health
def check_api_health():
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=5)
        if response.status_code == 200:
            return "Online", response.json()
        return "Error", {"status": "unhealthy"}
    except requests.exceptions.RequestException:
        return "Offline", {"status": "unreachable"}

# Helper: Donut chart
def make_donut(value, label, input_color="steelblue"):
    base = alt.Chart(alt.Data(values=[
        {"label": label, "value": value},
        {"label": "Remaining", "value": 100 - value}
    ]))
    chart = base.mark_arc(innerRadius=80, outerRadius=100).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(
            field="label", 
            type="nominal",
            scale=alt.Scale(
                domain=[label, "Remaining"], 
                range=[input_color, "#eee"]
            ),
            legend=None
        )
    )
    text = base.mark_text(radius=40, size=16).encode(
        text=alt.Text("value:Q", format=".2f")
    )
    return chart + text

# Header
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #00BFFF;'>💉 Insu Scan Pro 🩺</h1>
        <p>A Machine Learning Solution for Automating the Analysis of Medical Reports for Diabetes</p>
    </div>
""", unsafe_allow_html=True)

# Check API status
status, details = check_api_health()
st.session_state.api_status = status

# Sidebar
with st.sidebar:
    st.title("📋 Patient Details")
    
    # Add API status indicator
    status_color = {"Online": "green", "Offline": "red", "Error": "orange", "Unknown": "gray"}
    st.markdown(f"""
        <div style='display: flex; align-items: center;'>
            <div style='background-color: {status_color.get(status, "gray")}; 
                width: 12px; height: 12px; border-radius: 50%; margin-right: 8px;'></div>
            <span>API Status: {status}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if status != "Online":
        st.error("⚠️ Backend API is not reachable. Please ensure the FastAPI server is running.")
    
    patient_info = st.session_state.extracted_values
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Patient Name", value=patient_info.get("PatientName", ""), key="patient_name", disabled=True)
    with col2:
        st.text_input("Gender", value=patient_info.get("Gender", ""), key="gender", disabled=True)
    
    try:
        age_val = float(patient_info.get("Age", 0))
    except (ValueError, TypeError):
        age_val = 0
    
    st.number_input("Age", value=age_val, key="age", disabled=True)

    st.markdown("---")
    st.subheader("📊 Report Values")

    # Create two columns for numeric inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Pregnancies", value=float(patient_info.get("Pregnancies", 0)), key="preg", disabled=True)
        st.number_input("Blood Pressure", value=float(patient_info.get("BloodPressure", 0)), key="bp", disabled=True)
        st.number_input("Insulin", value=float(patient_info.get("Insulin", 0)), key="insulin", disabled=True)
        st.number_input("Diabetes Pedigree", value=float(patient_info.get("DiabetesPedigreeFunction", 0.0)), key="dpf", disabled=True)
    
    with col2:
        st.number_input("Glucose", value=float(patient_info.get("Glucose", 0)), key="glucose", disabled=True)
        st.number_input("Skin Thickness", value=float(patient_info.get("SkinThickness", 0)), key="skin", disabled=True)
        st.number_input("BMI", value=float(patient_info.get("BMI", 0.0)), key="bmi", disabled=True)

    st.markdown("---")
    st.subheader("📝 Notes")
    st.text_area("Doctor's Notes", value=patient_info.get("DoctorNotes", ""), key="notes", disabled=True, height=100)
    st.text_area("Diet Recommendation", value=patient_info.get("DietRecommendation", ""), key="diet", disabled=True, height=100)

# Main content area
st.subheader("📤 Upload Medical Report")

# File uploader with supported extensions
file = st.file_uploader("Upload medical report", type=["pdf", "docx", "txt"])

if file:
    # Store file content in session state to avoid re-uploading
    if "file_content" not in st.session_state or st.session_state.file_content is None:
        st.session_state.file_content = file.getvalue()
    
    # Get file type
    file_extension = file.name.split('.')[-1].lower()
    
    # Extract data button
    if st.button("🔍 Extract Data", key="extract_btn"):
        if st.session_state.api_status != "Online":
            st.error("⚠️ Cannot extract data: Backend API is not reachable.")
        else:
            with st.spinner("Extracting data from report..."):
                try:
                    files = {"file": (file.name, st.session_state.file_content, file.type)}
                    res = requests.post(EXTRACTION_URL, files=files, timeout=30)
                    
                    if res.status_code == 200:
                        data = res.json()
                        
                        if "error" in data:
                            st.error(f"Error from server: {data['error']}")
                        else:
                            st.session_state.extracted_values = data.get("extracted_values", {})
                            st.session_state.prediction_result = {
                                "prediction": data.get("prediction"),
                                "confidence": round(data.get("confidence", 0.0), 2),
                                "diabetes_type": data.get("diabetes_type"),
                                "summary": data.get("summary")
                            }
                            st.success("Data extracted successfully!")
                            # Force a rerun to update the sidebar values
                            st.rerun()
                    else:
                        st.error(f"Error: Extraction failed with status code {res.status_code}")
                        if res.text:
                            try:
                                error_data = res.json()
                                st.error(f"Server message: {error_data.get('error', 'Unknown error')}")
                            except json.JSONDecodeError:
                                st.error(f"Server response: {res.text[:200]}")
                                
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
                    st.info("Please check if the FastAPI backend is running.")

# Predict button
if st.session_state.extracted_values and st.button("🧠 Predict Diabetes", key="predict_btn"):
    if st.session_state.api_status != "Online":
        st.error("⚠️ Cannot make prediction: Backend API is not reachable.")
    else:
        with st.spinner("Predicting from extracted data..."):
            try:
                data = st.session_state.extracted_values
                response = requests.post(
                    PREDICTION_URL, 
                    json={"data": data},
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.session_state.prediction_result = response.json()
                    st.success("Prediction completed!")
                else:
                    st.error(f"Prediction failed with status code {response.status_code}")
                    try:
                        error_data = response.json()
                        st.error(f"Server message: {error_data.get('error', 'Unknown error')}")
                    except json.JSONDecodeError:
                        st.error(f"Server response: {response.text[:200]}")
                        
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
                st.info("Please check if the FastAPI backend is running.")

# Display Results
st.markdown("---")
if st.session_state.prediction_result and st.session_state.prediction_result.get("prediction") != "No Prediction":
    result = st.session_state.prediction_result
    prediction = result.get("prediction")
    confidence = result.get("confidence")
    diabetes_type = result.get("diabetes_type")
    summary = result.get("summary")

    # Create two columns for report preview and risk assessment
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📎 Report Preview")
        
        # Display file based on type
        if file and st.session_state.file_content:
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension in ['png', 'jpg', 'jpeg']:
                try:
                    image = Image.open(io.BytesIO(st.session_state.file_content))
                    st.image(image, use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying image: {str(e)}")
            
            elif file_extension == 'pdf':
                try:
                    # Import pdf2image only when needed
                    try:
                        from pdf2image import convert_from_bytes
                        
                        # Check if poppler path exists
                        poppler_path = "D:/ccc/poppler-24.08.0/Library/bin"
                        use_poppler = os.path.exists(poppler_path)
                        
                        # Convert PDF to images
                        if use_poppler:
                            pages = convert_from_bytes(st.session_state.file_content, poppler_path=poppler_path)
                        else:
                            pages = convert_from_bytes(st.session_state.file_content)
                        
                        # Display total pages info
                        total_pages = len(pages)
                        st.info(f"PDF: {total_pages} page{'s' if total_pages > 1 else ''}")
                        
                        # Page navigation
                        if total_pages > 1:
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                if st.button("⬅️ Previous") and st.session_state.page_number > 0:
                                    st.session_state.page_number -= 1
                                    st.experimental_rerun()
                            with col2:
                                if st.button("Next ➡️") and st.session_state.page_number < total_pages - 1:
                                    st.session_state.page_number += 1
                                    st.experimental_rerun()
                            
                            # Current page display
                            page_num = min(st.session_state.page_number, total_pages - 1)
                            st.caption(f"Page {page_num + 1} of {total_pages}")
                        else:
                            page_num = 0
                        
                        # Show current page
                        st.image(pages[page_num], use_container_width=True)
                        
                    except ImportError:
                        st.warning("PDF preview unavailable. Please install pdf2image and poppler.")
                        st.info("If using Windows, download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/")
                        st.code("pip install pdf2image")
                        
                except Exception as e:
                    st.error(f"Error rendering PDF: {str(e)}")
                    st.info("Please make sure Poppler is installed correctly if you're on Windows.")
            
            elif file_extension in ['docx', 'txt']:
                st.info(f"Preview not available for {file_extension.upper()} files")
                st.download_button(
                    label=f"Download {file.name}",
                    data=st.session_state.file_content,
                    file_name=file.name,
                    mime=file.type
                )
        else:
            st.info("Upload a file to preview it")

    with col2:
        st.subheader("📊 Risk Assessment")
        
        # Determine color based on prediction
        chart_color = "crimson" if prediction == "Diabetes" else "steelblue"
        
        # Create and display donut chart
        donut = make_donut(confidence, "Diabetes Risk", input_color=chart_color)
        st.altair_chart(donut, use_container_width=True)
        
        # Results display
        risk_color = "red" if prediction == "Diabetes" else "green"
        st.markdown(f"**📌 Prediction**: <span style='color:{risk_color};font-weight:bold'>{prediction}</span>", unsafe_allow_html=True)
        st.markdown(f"**🎯 Confidence**: `{confidence:.2f}%`")
        
        if prediction == "Diabetes":
            st.markdown(f"**🩺 Type**: `{diabetes_type}`")
            
            # Add risk factors explanation
            st.markdown("### Risk Factors")
            
            # Check for high glucose
            if st.session_state.extracted_values.get("Glucose", 0) > 126:
                st.warning("⚠️ High fasting glucose detected (>126 mg/dL)")
            
            # Check for high BMI
            bmi = st.session_state.extracted_values.get("BMI", 0)
            if bmi > 30:
                st.warning(f"⚠️ Obesity detected (BMI: {bmi:.1f})")
            elif bmi > 25:
                st.info(f"ℹ️ Overweight (BMI: {bmi:.1f})")
                
            # Check for family history
            dpf = st.session_state.extracted_values.get("DiabetesPedigreeFunction", 0)
            if dpf > 0.8:
                st.warning(f"⚠️ Strong family history factor ({dpf:.2f})")

    # Summary section
    st.markdown("---")
    st.subheader("📃 AI Report Summary")
    st.markdown(summary, unsafe_allow_html=True)
    
    # Add action buttons for the report
    col1, col2 = st.columns([1, 1])
    with col1:
        # Create a button to download the summary as a text file
        if st.button("📥 Download Summary"):
            report_text = summary.replace('**', '').replace('*', '')
            st.download_button(
                label="Save Summary as Text",
                data=report_text,
                file_name=f"diabetes_report_{int(time.time())}.txt",
                mime="text/plain"
            )   
    with col2:
        # Print option
        if st.button("🖨️ Print Report"):
            st.info("Please use your browser's print function (Ctrl+P / Cmd+P)")
            st.markdown(
                """
                <style>
                @media print {
                    .stApp { display: none; }
                    #print-content { display: block; }
                }
                </style>
                <div id="print-content" style="display:none;">
                    <h2>Diabetes Analysis Report</h2>
                    <pre>{}</pre>
                </div>
                """.format(summary.replace('<', '&lt;').replace('>', '&gt;')),
                unsafe_allow_html=True
            )

else:
    # Show instructions when no prediction is available
    st.info("👆 Upload a medical report and click 'Extract Data' to analyze diabetes risk.")
    
    # Display example image
    st.markdown("### How to use Insu Scan Pro:")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        1. **Upload** your medical report (PDF, DOCX, or TXT)
        2. Click **Extract Data** to analyze the report
        3. Review the extracted values in the sidebar
        4. Click **Predict Diabetes** to get an AI assessment
        5. Download or share your analysis report
        """)
    
    with col2:
        st.markdown("""
        **Supported Data Points:**
        - Patient demographics (Age, Gender)
        - Blood glucose levels
        - Blood pressure
        - BMI (Body Mass Index)
        - Insulin levels
        - Family history (Diabetes Pedigree Function)
        - Doctor's notes and recommendations
        """)


