<p align="center">
  <img src="https://github.com/SharmAnshu5/InsuScan_Pro/blob/main/Portfolio%20(1).png" alt="InsuScan Pro Banner" width="100%">
</p>

<h1 align="center">💉 InsuScan Pro 🩺</h1>
<p align="center"><strong>A Machine Learning Solution for Automating the Analysis of Medical Reports for Diabetes</strong></p>

<p align="center">
  <i>Transforming traditional reports into smart insights in just one click.</i>
</p>

---

<p align="center">
  <img src="https://github.com/SharmAnshu5/InsuScan_Pro/blob/main/New%20folder/Screenshot%202025-05-13%20200619.png" alt="InsuScan Pro preview" width="100%">
</p>


---

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" /></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi" /></a>
  <a href="https://xgboost.readthedocs.io/"><img src="https://img.shields.io/badge/XGBoost-Model-orange?logo=sklearn" /></a>
  <a href="https://shap.readthedocs.io/"><img src="https://img.shields.io/badge/SHAP-ExplainableAI-purple?logo=plotly" /></a>
  <a href="https://github.com/"><img src="https://img.shields.io/badge/License-MIT-lightgrey" /></a>
</p>

---

## 🚀 Live Demo & Resources

<p align="center">
  🔗 <strong>Live App</strong>: comming soon
  <br>
  📽️ <strong>Demo Video</strong>: [Watch Demo](https://youtu.be/Zql4xyS1fs4)  
  <br>
  📊 <strong>Dataset</strong>: [PIMA Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)
</p>

---

## 🧠 Project Overview

**Insu Scan Pro** bridges the gap between raw medical data and AI-powered interpretation:

- Extracts structured data from PDF/DOCX reports
- Predicts diabetes using **XGBoost**
- Explains predictions using **SHAP**
- Generates natural-language summaries for readability

This aids both **patients** and **doctors** in understanding health conditions and enables **quicker diagnoses**.

---

## 📦 Key Features

✅ Upload reports in **PDF, DOCX, or TXT**  
✅ Auto-extract values like **Glucose, Insulin, Age, BMI**  
✅ Predict **Diabetes Type 1 / Type 2** with confidence  
✅ View **SHAP waterfall plot** for explainability  
✅ Get **plain English AI-generated summaries**  
✅ Extract **doctor notes** and **diet plans**  
✅ User-friendly **Streamlit frontend**

---

## 🧠 Machine Learning & AI

### 🎯 Model: XGBoost Classifier

A robust gradient boosting algorithm for tabular data:

- Handles missing values
- Regularized (L1/L2) to prevent overfitting
- Feature importance & SHAP visualization
- Efficient parallel training

### 📊 Features Extracted

- `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`
- `BMI`, `DiabetesPedigreeFunction`, `Age`

### 🧮 AI Insights

- SHAP explains each prediction via feature contribution
- Generates natural summaries in human language

---

## 📂 Folder Structure

```
InsuScan_Pro
│ LICENSE
│ README.md
│ requirements.txt
│
├───backend
│ ├── main.py
│ ├── data/
│ ├── models/
│ ├── services/models/
│ ├── utils/
│ └── pycache/
│
└───frontend
└── app.py


```

---

## 🛠️ Local Development Guide

### 🔧 Clone the Repo

```

git clone https://github.com/your-username/insu-scan-pro.git
cd insu-scan-pro
```
📦 Setup Python Virtual Env

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```
📁 Backend: FastAPI

```
cd backend
uvicorn main:app --reload

```
🌐 Frontend: Streamlit

```
cd ../frontend
streamlit run app.py
```

💡 Ensure http://localhost:8000 is used in frontend for backend API calls.

📄 Dataset
Source: UCI ML Repository

Used for: Diabetes diagnosis prediction

Link: PIMA Indians Dataset

📜 License
Distributed under the MIT License. See LICENSE for details.

👨‍💻 Author
<p align="center"> 
        <b>Anshu Sharma</b><br> 🎓 Final-year Computer Science & AI Student <br> <a href="https://github.com/SharmAnshu5">GitHub</a> | <a href="https://www.linkedin.com/in/anshu-sharma-b74a07221/">LinkedIn</a> </p>
