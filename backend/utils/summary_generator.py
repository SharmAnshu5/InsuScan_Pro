def generate_summary(data, prediction, confidence, diabetes_type):
    """
    Generate a formatted summary of the diabetes analysis

    Parameters:
    - data: Dictionary containing patient data
    - prediction: Binary prediction (0 or 1) or string ('Diabetes'/'No Diabetes')
    - confidence: Confidence score (0-100)
    - diabetes_type: String indicating diabetes type

    Returns:
    - Formatted summary string
    """
    # Handle potential None or invalid values
    if not isinstance(data, dict):
        data = {}

    # Extract patient information with safe defaults
    name = data.get("PatientName", "The patient")
    if name == "N/A" or not name.strip():
        name = "The patient"

    gender = data.get("Gender", "N/A")

    # Handle age safely - could be string or number
    age = data.get("Age", "N/A")
    try:
        age = float(age)
        age_str = f"{int(age)} years"
    except (ValueError, TypeError):
        age_str = "Age not specified"

    notes = data.get("DoctorNotes", "No notes provided.")
    if not notes or notes.lower() in ["not provided", "n/a"]:
        notes = "No specific notes provided by the doctor."

    diet = data.get("DietRecommendation", "None provided.")
    if not diet or diet.lower() in ["not specified", "n/a"]:
        diet = "No specific diet recommendations provided."

    # Determine diagnosis based on glucose level
    glucose = data.get("Glucose", 0)
    try:
        glucose = float(glucose)
        if glucose > 140:
            diagnosis = "🔴 Elevated glucose levels detected"
        elif glucose > 100:
            diagnosis = "🟠 Borderline glucose levels"
        else:
            diagnosis = "🟢 Normal glucose levels"
    except (ValueError, TypeError):
        diagnosis = "⚠️ Glucose levels not available"

    # Handle prediction
    if isinstance(prediction, bool):
        has_diabetes = prediction
    elif isinstance(prediction, int):
        has_diabetes = prediction == 1
    elif isinstance(prediction, str):
        has_diabetes = prediction.lower() in ("diabetes", "yes", "true", "positive", "1")
    else:
        has_diabetes = False

    # Format confidence
    try:
        confidence_val = float(confidence)
        confidence_str = f"{confidence_val:.2f}%"
    except (ValueError, TypeError):
        confidence_str = "unknown confidence"

    # Start summary
    summary = (
        f"🔬 **Summary for {name}**\n"
        f"----------------------------------------\n"
        f"📅 **Age**: {age_str}\n"
        f"👤 **Gender**: {gender}\n"
        f"🧪 **Diagnosis**: {diagnosis}\n\n"
        f"📌 **Key Health Indicators:**\n"
    )

    if glucose:
        summary += f"• Glucose Level: {glucose} mg/dL\n"

    if data.get('BMI'):
        summary += f"• BMI: {data['BMI']} kg/m²\n"

    if data.get('DiabetesPedigreeFunction'):
        summary += f"• Family History Score: {data['DiabetesPedigreeFunction']}\n"

    summary += (
        f"\n📝 **Doctor's Notes:**\n"
        f"{notes}\n\n"
        f"🍽️ **Diet Recommendations:**\n"
        f"{diet}\n\n"
        f"✅ **How to Stay Healthy:**\n"
        f"• Eat more whole grains, fruits, and vegetables.\n"
        f"• Limit sugary snacks and drinks.\n"
        f"• Get 30 minutes of daily physical activity.\n"
        f"• Monitor your sugar levels regularly.\n"
        f"• Get regular medical check-ups.\n\n"
        f"💡 *Early action can help prevent complications and lead to a healthier life.*\n"
    )

    if has_diabetes:
        summary += (
            f"\n⚠️ **Prediction Result:**\n"
            f"The model predicts a **high risk of diabetes** with **{confidence_str}** confidence.\n"
            f"\n🧾 **Diabetes Type:** {diabetes_type}\n"
        )
    else:
        summary += (
            f"\n✅ **Prediction Result:**\n"
            f"The model predicts **no significant risk** of diabetes with **{confidence_str}** confidence.\n"
        )

    summary += (
        f"\n💬 **Health Tips:**\n"
        f"\n• Maintain a healthy diet and exercise regularly.\n"
        f"\n• Monitor glucose levels.\n"
        f"\n• Consult your physician for routine checkups.\n"
    )

    return summary
