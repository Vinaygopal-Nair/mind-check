# 🧠 Mind Check: PHQ-9 Depression Screening App

Welcome to **Mind Check** — a simple, interactive mental health screening tool based on the clinically backed **PHQ-9 questionnaire**. Built with **Streamlit**, this app calculates your depression severity, includes optional age/gender inputs, and features a **truth matrix** to evaluate model reliability using CSV data.

---

## 🚀 Features

✅ **PHQ-9 Questionnaire**  
The standard 9-question self-assessment used by professionals to screen for depression.

✅ **Instant Scoring**  
Automatically calculates depression severity levels (None, Mild, Moderate, etc.)

✅ **Truth Matrix Support**  
Upload actual vs. predicted results in a CSV to generate a **confusion matrix** and detailed **classification report**.

✅ **User Inputs**  
Collects age and gender (optional) to allow for personalized future advice.

✅ **Streamlit Interface**  
Fast, clean, and easy to use on any browser — no installs needed for end users.

---

## 🛠️ How to Run the App Locally

Make sure Python and Streamlit are installed. Then:

```bash
git clone https://github.com/Vinaygopal-Nair/mind-check.git
cd mind-check
pip install -r requirements.txt
streamlit run app.py
