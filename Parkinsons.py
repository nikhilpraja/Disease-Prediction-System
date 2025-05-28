# Personal Code: DPS-PARK-004
# Author: [Your Name]
# Description: Parkinson's disease prediction page using voice measurements with standardized input form and consistent UI design.

import streamlit as st
import pandas as pd
import joblib
import os

def show_parkinsons_page():
    # Check for model, scaler, and feature names files
    model_path = "C:/Users/91787/Downloads/parkinsons_model.pkl"
    scaler_path = "C:/Users/91787/Downloads/parkinsons_scaler.pkl"
    feature_names_path = "C:/Users/91787/Downloads/parkinsons_feature_names.pkl"
    
    if not all(os.path.exists(path) for path in [model_path, scaler_path, feature_names_path]):
        st.error("⚠️ Model, scaler, or feature names file not found. Please ensure files are in the 'models' directory.")
        return
    
    # Load model, scaler, and feature names
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(feature_names_path)
    except Exception as e:
        st.error(f"Error loading model, scaler, or feature names: {str(e)}")
        return

    # Page header
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Parkinson's Disease Prediction</h1>", unsafe_allow_html=True)


    # Feature labels
    feature_labels = {
        'MDVP:Fo(Hz)': 'Average Voice Frequency (Hz)',
        'MDVP:Fhi(Hz)': 'Highest Voice Frequency (Hz)',
        'MDVP:Flo(Hz)': 'Lowest Voice Frequency (Hz)',
        'MDVP:Jitter(%)': 'Voice Frequency Variation (%)',
        'MDVP:Jitter(Abs)': 'Absolute Voice Frequency Variation (ms)',
        'MDVP:RAP': 'Rapid Voice Frequency Variation',
        'MDVP:PPQ': 'Voice Frequency Stability',
        'Jitter:DDP': 'Detailed Voice Frequency Variation',
        'MDVP:Shimmer': 'Voice Amplitude Variation',
        'MDVP:Shimmer(dB)': 'Voice Amplitude Variation (dB)',
        'Shimmer:APQ3': 'Short-Term Voice Amplitude Variation 1',
        'Shimmer:APQ5': 'Short-Term Voice Amplitude Variation 2',
        'MDVP:APQ': 'Long-Term Voice Amplitude Variation',
        'Shimmer:DDA': 'Detailed Voice Amplitude Variation',
        'NHR': 'Noise-to-Harmonics Ratio',
        'HNR': 'Harmonics-to-Noise Ratio',
        'RPDE': 'Voice Complexity Measure 1',
        'DFA': 'Voice Complexity Measure 2',
        'spread1': 'Voice Spread Measure 1',
        'spread2': 'Voice Spread Measure 2',
        'D2': 'Voice Dynamics Measure',
        'PPE': 'Voice Pitch Entropy'
    }

    # Input form
    with st.form(key="parkinsons_form"):
        st.markdown("### 🧾 Voice Measurements")
        cols = st.columns(3)
        inputs = {}
        for idx, feature in enumerate(feature_names):
            with cols[idx % 3]:
                label = feature_labels.get(feature, feature)
                inputs[feature] = st.number_input(
                    label, min_value=0.0, value=0.0, step=0.0001, format="%.6f", help="Enter a non-negative value", key=feature
                )
        
        submit = st.form_submit_button("🔍 Predict", use_container_width=True)
        
        if submit:
            if any(value < 0 for value in inputs.values()):
                st.error("All values must be non-negative.")
            elif all(value == 0 for value in inputs.values()):
                st.error("Please enter at least one non-zero value.")
            else:
                try:
                    input_data = pd.DataFrame([inputs], columns=feature_names)
                    input_scaled = scaler.transform(input_data)
                    prediction = model.predict(input_scaled)[0]
                    probability = model.predict_proba(input_scaled)[0][prediction] * 100
                    result = "🟥 Parkinson's Disease" if prediction == 1 else "🟩 Healthy"
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
                            st.error("High risk of Parkinson's disease. Please consult a neurologist.")
                        else:
                            st.success("Low risk of Parkinson's disease. Maintain a healthy lifestyle.")
                    
                    with st.expander("📊 Detailed Probabilities"):
                        st.write(f"Probability of Healthy: **{model.predict_proba(input_scaled)[0][0]*100:.1f}%**")
                        st.write(f"Probability of Parkinson's: **{model.predict_proba(input_scaled)[0][1]*100:.1f}%**")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
    
    # Feature descriptions
    with st.expander("ℹ️ About Voice Measurements"):
        for feature, label in feature_labels.items():
            st.markdown(f"- **{label}**: {feature_labels.get(feature, 'No description available.')}")