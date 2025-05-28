# Personal Code: DPS-HEART-003
# Author: [Your Name]
# Description: Heart disease prediction page using a trained model with standardized input form and consistent UI design.

import streamlit as st
import numpy as np
import joblib
import os

def show_heart_disease_page():
    # Check for model, scaler, and imputer files
    model_path = "C:/Users/91787/Downloads/heart_disease_model.pkl"
    scaler_path = "C:/Users/91787/Downloads/scaler_heart.pkl"
    imputer_path = "C:/Users/91787/Downloads/imputer.pkl"
    
    if not all(os.path.exists(path) for path in [model_path, scaler_path, imputer_path]):
        st.error("⚠️ Model, scaler, or imputer file not found. Please ensure files are in the 'models' directory.")
        return
    
    # Load model, scaler, and imputer
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        imputer = joblib.load(imputer_path)
    except Exception as e:
        st.error(f"Error loading model, scaler, or imputer: {str(e)}")
        return

    # Page header
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Heart Disease Prediction</h1>", unsafe_allow_html=True)


    # Input form
    with st.form(key="heart_disease_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=50, help="Age in years")
            sex = st.selectbox("Gender", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male", help="Biological sex")
            cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], format_func=lambda x: ["None", "Typical Angina", "Atypical Angina", "Asymptomatic"][x], help="Type of chest pain")
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, value=120, help="Resting blood pressure")
            chol = st.number_input("Cholesterol (mg/dl)", min_value=0, value=200, help="Serum cholesterol")
            fbs = st.selectbox("Fasting Blood Sugar", [0, 1], format_func=lambda x: "Normal" if x == 0 else "High (>120 mg/dl)", help="Fasting blood sugar level")
            restecg = st.selectbox("Resting ECG Result", [0, 1, 2], format_func=lambda x: ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"][x], help="Electrocardiogram result")
     
        with col2:
            thalach = st.number_input("Max Heart Rate", min_value=0, value=150, help="Maximum heart rate achieved")
            exang = st.selectbox("Exercise-Induced Chest Pain", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Chest pain during exercise")
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1, help="ST depression induced by exercise")
            slope = st.selectbox("ST Segment Slope", [0, 1, 2], format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x], help="Slope of the peak exercise ST segment")
            ca = st.number_input("Major Vessels Blocked (0-4)", min_value=0, max_value=4, value=0, help="Number of major vessels colored by fluoroscopy")
            thal = st.selectbox("Thalassemia Result", [0, 1, 2, 3], format_func=lambda x: ["Not Tested", "Normal", "Fixed Defect", "Reversible Defect"][x], help="Thalassemia test result")
        
        submit = st.form_submit_button("🔍 Predict", use_container_width=True)
        
        if submit:
            try:
                input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
                input_data_imputed = imputer.transform(input_data)
                input_data_scaled = scaler.transform(input_data_imputed)
                prediction = model.predict(input_data_scaled)[0]
                probability = model.predict_proba(input_data_scaled)[0][prediction] * 100
                result = "🟥 High Risk (Heart Disease)" if prediction == 1 else "🟩 Low Risk (No Heart Disease)"
                color = "#C0392B" if prediction == 1 else "#27AE60"
                
                st.markdown(
                    f"<div style='text-align: center; margin-top: 20px;'>"
                    f"<h3 style='color: {color};'>Prediction: {result}</h3>"
                    f"<p style='font-size: 18px;'>Confidence: <strong>{probability:.1f}%</strong></p>"
                    "</div>",
                    unsafe_allow_html=True
                )
                
                with st.expander("🔎 What This Means"):
                    if prediction == 1:
                        st.error("High risk of heart disease. Please consult a cardiologist.")
                    else:
                        st.success("Low risk of heart disease. Maintain a healthy lifestyle.")
                
                with st.expander("📊 Detailed Probabilities"):
                    st.write(f"Probability of No Heart Disease: **{model.predict_proba(input_data_scaled)[0][0]*100:.1f}%**")
                    st.write(f"Probability of Heart Disease: **{model.predict_proba(input_data_scaled)[0][1]*100:.1f}%**")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")