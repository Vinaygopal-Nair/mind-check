import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# Set page title and icon
st.set_page_config(page_title="PHQ-9 Depression Test", page_icon="🧠")

st.title("🧠 PHQ-9 Depression Self-Assessment")
st.subheader("👤 Personal Info")

# Gender and Age Inputs with no default selection
gender = st.selectbox("Select your gender:", ["Select", "Male", "Female", "Other"], index=0)
age = st.number_input("Enter your age:", min_value=10, max_value=100, step=1)

# Mode Selection
mode = st.selectbox("Choose a mode:", ["Standard PHQ-9", "The Real Feel Test"], index=0)

# Session state for submission
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Shared options dictionary
options = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

# To store latest results for export
user_result = {}

if mode == "Standard PHQ-9":
    st.header("📝 PHQ-9 Depression Questionnaire")

    phq9_questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure",
        "Trouble concentrating on things",
        "Moving or speaking slowly, or being fidgety/restless",
        "Thoughts that you would be better off dead"
    ]

    phq_responses = []
    for i, q in enumerate(phq9_questions):
        response = st.radio(q, list(options.keys()), key=f"phq_{i}", index=None)
        phq_responses.append(options[response] if response else None)

    if not st.session_state.submitted:
        if st.button("Submit"):
            if None in phq_responses:
                st.warning("⚠️ Please answer all 9 questions before submitting.")
            else:
                score = sum(phq_responses)

                if score <= 4:
                    level = "Minimal or None"
                elif score <= 9:
                    level = "Mild"
                elif score <= 14:
                    level = "Moderate"
                elif score <= 19:
                    level = "Moderately Severe"
                else:
                    level = "Severe"

                st.session_state.submitted = True

                st.success(f"✅ Your PHQ-9 Score: {score}")
                st.markdown(f"### 📊 Depression Severity: **{level}**")
                st.info("📜 This result is for self-assessment only. Please consult a licensed mental health professional for a full evaluation.")

                user_result = {
                    "Gender": gender,
                    "Age": age,
                    "Mode": mode,
                    "Score": score,
                    "Severity": level
                }

                # Suggestions block
                if score <= 4:
                    st.success("You're doing okay! Stay mindful and nurture healthy habits.")
                elif score <= 9:
                    st.warning("You may be experiencing mild symptoms. Keep journaling, talking to close ones, and resting well.")
                elif score <= 14:
                    st.error("You're showing signs of moderate depression.")
                    st.markdown("""
                    **Here’s what may help:**
                    - 🏃‍♂️ Light workouts or evening walks
                    - 💬 Talk to a friend, mentor, or therapist
                    - 👕 Try journaling thoughts and emotions
                    - 📵 Reduce screen time, especially late night
                    - 🌟 Try to build a 3-step daily routine
                    """)
                elif score <= 19:
                    st.error("You're showing signs of moderately severe depression.")
                    st.markdown("""
                    **Consider these steps:**
                    - 🧘 Practice mindfulness or guided breathing
                    - 📱 Reduce time on social media
                    - 🧑‍⚕️ Reach out to a professional counselor or helpline
                    - 📚 Engage in any small learning task or hobby
                    """)
                else:
                    st.error("This score indicates severe depression.")
                    st.markdown("""
                    **Important:** Please seek support urgently.
                    - 📞 Reach out to a helpline or mental health expert
                    - 🦦 Try to stay around people you trust
                    - 🤝 You're not alone. Let someone know what you're going through
                    """)

                st.download_button("📄 Export Result as CSV", data=pd.DataFrame([user_result]).to_csv(index=False), file_name="phq9_result.csv", mime="text/csv")
                if st.button("🔄 Retake Test"):
                    st.session_state.submitted = False
                    st.experimental_rerun()
    else:
        st.info("🔐 You've already submitted your responses. Refresh the page or click Retake Test to try again.")

# --------------------------
# 📊 TRUTH MATRIX (ADVANCED)
# --------------------------
with st.expander("📊 Advanced: Model Reliability - Truth Matrix"):
    uploaded_file = st.file_uploader("Upload CSV with actual labels & PHQ-9 scores", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["predicted_label"] = df["phq9_score"].apply(lambda x: 1 if x >= 10 else 0)

        cm = confusion_matrix(df["actual_label"], df["predicted_label"])
        report = classification_report(df["actual_label"], df["predicted_label"], output_dict=True)

        st.subheader("Confusion Matrix")
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Not Depressed", "Depressed"],
                    yticklabels=["Not Depressed", "Depressed"])
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        st.pyplot(fig)

        st.subheader("Classification Report")
        st.write(report)
        st.json(report)

        metrics = ["precision", "recall", "f1-score"]
        labels = [label for label in report if label in ['0', '1']]
        data = {
            metric: [report[label][metric] for label in labels]
            for metric in metrics
        }

        x = np.arange(len(labels))
        width = 0.25

        fig, ax = plt.subplots()
        ax.bar(x - width, data["precision"], width, label="Precision", color="#4CAF50")
        ax.bar(x, data["recall"], width, label="Recall", color="#2196F3")
        ax.bar(x + width, data["f1-score"], width, label="F1-Score", color="#FFC107")

        ax.set_ylabel("Score")
        ax.set_title("📊 Classification Metrics by Class")
        ax.set_xticks(x)
        ax.set_xticklabels(["Not Depressed (0)", "Depressed (1)"])
        ax.set_ylim(0, 1.1)
        ax.legend()

        st.pyplot(fig)
    else:
        st.info("📂 Upload a CSV file above to view the truth matrix and performance report.")




