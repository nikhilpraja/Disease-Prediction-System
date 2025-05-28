# Personal Code: DPS-DIAB-002
# Author: [Your Name]
# Description: Diabetes prediction page using KNN model with standardized input form and consistent UI design.

import streamlit as st
import pandas as pd
import joblib
import os

def show_diabetes_page():
    # Check for model and scaler files
    model_path = "knn_diabetes_model.pkl"
    scaler_path = "scaler.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error("⚠️ Model or scaler file not found. Please ensure 'knn_diabetes_model.pkl' and 'scaler.pkl' are in the 'models' directory.")
        return
    
    # Load model and scaler
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        st.error(f"Error loading model or scaler: {str(e)}")
        return

    # Page header
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Diabetes Prediction</h1>", unsafe_allow_html=True)

    # Input form
    with st.form(key="diabetes_form"):
        st.markdown("### 🧾 Health Data")
        col1, col2 = st.columns(2)
        
        with col1:
            pregnancies = st.number_input("Number of Pregnancies ", min_value=0, max_value=20, value=0, help="Number of times pregnant")
            glucose = st.number_input("Glucose (mg/dl)", min_value=0.0, value=100.0, help="Plasma glucose concentration")
            blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, value=70.0, help="Diastolic blood pressure")
            skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, value=20.0, help="Triceps skin fold thickness")
        
        with col2:
            insulin = st.number_input("Insulin (mu U/ml)", min_value=0.0, value=80.0, help="2-Hour serum insulin")
            bmi = st.number_input("BMI", min_value=0.0, value=30.0, help="Body mass index (kg/m²)")
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, value=0.5, help="Family history of diabetes")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=30, help="Age in years")
        
        submit = st.form_submit_button("🔍 Predict", use_container_width=True)
        
        if submit:
            try:
                input_data = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]]
                input_scaled = scaler.transform(input_data)
                prediction = model.predict(input_scaled)[0]
                result = "🟥 Diabetic" if prediction == 1 else "🟩 Not Diabetic"
                color = "#C0392B" if prediction == 1 else "#27AE60"
                
                st.markdown(
                    f"<div style='text-align: center; margin-top: 15px;'>"
                    f"<h3 style='color: {color};'>Prediction: {result}</h3>"
                    "</div>",
                    unsafe_allow_html=True
                )
                
                with st.expander("🔎 What This Means"):
                    if prediction == 1:
                        st.error("High risk of diabetes. Please consult a doctor.")
                    else:
                        st.success("Low risk of diabetes. Maintain a healthy lifestyle.")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")