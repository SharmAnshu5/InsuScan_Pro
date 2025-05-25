# InsuScan_Pro
A Machine Learning Solution for Automating the Analysis of Medical Reports for Diabetes

**Insu Scan Pro** is an intelligent, end-to-end web application designed to assist patients and medical professionals by automatically reading diabetic medical reports, extracting vital clinical data, performing machine learning-based predictions, and understandably explaining the results using SHAP visualisations and natural summaries.

> It transforms traditional PDF/DOCX lab reports into interactive, AI-driven insights — all in one click.


---

![App Screenshot](https://github.com/SharmAnshu5/InsuScan_Pro/blob/main/New%20folder/Screenshot%202025-05-13%20200619.png)

---


## 🚀 Live Demo & Resources

* 🌐 **Live App**: [https://your-deployment-link.com](https://your-deployment-link.com)
* 🎥 **Demo Video (MP4)**: [Watch Demo](https://youtu.be/D9VmF_uKr5k)
* 📊 **Dataset**: [PIMA Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

---

## 🧠 Project Overview

The core idea of **Insu Scan Pro** is to bridge the gap between raw medical data and its meaningful interpretation. The application uses:

* **Document parsing libraries** to extract structured data from medical reports (PDF, DOCX, TXT).
* **Machine Learning (XGBoost)** to predict diabetes based on extracted features.
* **Explainable AI (SHAP)** to visually represent the factors influencing predictions.
* **Natural Language Generation** to provide easy-to-read summaries of the reports.

This helps patients **understand their health condition** and supports medical staff in **quick report analysis**, reducing manual effort and error.

---

## 📦 Key Features

✅ Upload medical reports in **PDF, DOCX, or TXT** formats
✅ Automatically extract values like **Glucose, Insulin, Age, BMI**, etc.
✅ Predict **whether the patient has diabetes**, and if so, **Type 1 or Type 2**
✅ Display **confidence score** and **SHAP Waterfall Plot** for explanation
✅ Generate a **summary of results in plain English**
✅ Extract **Doctor's Notes** and **Diet Recommendations**
✅ **Streamlit UI** with modern, responsive layout and sidebar

---

## 🧠 Machine Learning & AI Models

### 🎯 Model Used: **XGBoost Classifier**

* A powerful **gradient boosting decision tree** algorithm known for its **high performance on tabular data**.
* It combines the output of multiple decision trees and optimizes based on gradient descent, making it **more accurate than individual classifiers like Logistic Regression or SVM**.

### ✅ Why XGBoost?

* Handles missing data gracefully
* Regularized model (L1 & L2) to prevent overfitting
* Supports feature importance and visualisation
* Fast and efficient due to parallelised tree boosting

### 📊 Features Used from Reports:

* `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`

### 🧮 Under the Hood:

* **Decision Trees**: Core building blocks used in boosting.
* **Gradient Boosting**: Models are trained sequentially, each correcting the previous.
* **SHAP (SHapley Additive exPlanations)**: Used to **interpret model predictions** by attributing contributions of each feature to the final decision.

---

## 🧰 Technologies Used

| Category                | Libraries / Tools                                                          |
| ----------------------- | -------------------------------------------------------------------------- |
| **Frontend**            | Streamlit, Plotly, Matplotlib                                              |
| **Backend API**         | FastAPI                                                                    |
| **ML & Data Science**   | XGBoost, Scikit-learn, Pandas, SHAP                                        |
| **Document Processing** | PyMuPDF (fitz), python-docx, IPython                                       |
| **File Handling**       | `multipart/form-data`, base64 encoding                                     |
| **Visualization**       | Donut Charts, Streamlit animation                                          |
| **Deployment**          | Streamlit Sharing / HuggingFace / Render (Choose based on your deployment) |

> We use **PyMuPDF** for accurate PDF text extraction, even for reports with varying layouts, and `python-docx` for parsing DOCX files.
> Also use "Popular " for the preview of medical report

---

## 📂 Folder Structure

```
InsuScan_Pro
│   LICENSE
│   README.md
│   requirements.txt
│
├───backend
│   │   main.py
│   │
│   ├───data
│   │       diabetes_dataset.csv
│   │
│   ├───models
│   │       diabetes_model.pkl
│   │
│   ├───services
│   │   ├───models
│   │   │       diabetes_xgb_model.pkl
│   │   │       scaler.pkl
│   │   │       scheams.py
│   │   │
│   │   └───__pycache__
│   │           diabetes_classifier.cpython-312.pyc
│   │
│   ├───utils
│   │   │   extract_diabetes_data.py
│   │   │   model_loader.py
│   │   │   summary_generator.py
│   │   │
│   │   └───__pycache__
│   │           extract_diabetes_data.cpython-312.pyc
│   │           extract_diabetes_data.cpython-313.pyc
│   │           summary_generator.cpython-312.pyc
│   │           summary_generator.cpython-313.pyc
│   │
│   └───__pycache__
│           main.cpython-312.pyc
│           main.cpython-313.pyc
│
└───frontend
        app.py
```

---

## 💻 How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/insu-scan-pro.git
cd insu-scan-pro
```
### 2. Setup project (Popular_path)
*Install all dependancies from requirements.txt
*For pdf2image you need to download poppler
*Install Tesseract OCR Engine in your PC
*Tesseract installation instrution : Github
*Tesseract windows specific instructions: Github
*Set required PATHs as per your environment

### 2. Setup project (Virtual Enviorment)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Setup backend (FastApi)

```bash
cd backend
uvicorn main:app --reload
```

### 4. Setup Frontend (Streamlit)

```bash
cd ../frontend
streamlit run app.py
```

* Make sure the backend URL is configured correctly in your frontend file (e.g., `http://localhost:8000`).

---

## 🧪 Dataset Used

* **Source**: UCI ML Repository via Kaggle
* **Link**: [PIMA Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

This dataset contains diagnostic measurements and outcomes for female patients of Pima Indian heritage and is widely used for binary diabetes classification.

---

## 📜 License

This project is licensed under the **MIT License**.
Feel free to use, modify, and distribute. See [`LICENSE`](LICENSE) file for more details.

---

## 🙋‍♂️ Author

**Anshu Sharma**
🎓 Final-year Computer Science & AI Student
🔗 [GitHub](https://github.com/SharmAnshu5) | [LinkedIn](https://www.linkedin.com/in/anshu-sharma-b74a07221/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---

## 💬 Feedback & Contribution

Want to improve this app? Found a bug?
Pull requests and issues are welcome. Let's build something impactful together!
