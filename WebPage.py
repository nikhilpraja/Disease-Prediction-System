
import streamlit as st
import json
import hashlib
import os
from main import show_diabetes_page
from Heart_Disease.Heart_Disease import show_heart_disease_page
from Parkinsons import show_parkinsons_page

# Streamlit configuration
st.set_page_config(page_title="Disease Prediction System", layout="wide", page_icon="🏥")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Users file setup
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🏥 Disease Prediction System")
    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("Logged out successfully!")
    else:
        st.info("🔓 Please log in to access all features.")
    menu = st.radio("📋 Navigation", ["🏠 Home", "👤 Profile", "🔬 Disease Prediction"])

# Home page
if menu == "🏠 Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://img.freepik.com/free-vector/hospital-logo-design-vector-medical-cross_53876-136743.jpg", use_container_width=True)
    with col2:
        st.markdown("## 👨‍⚕️ Disease Prediction System")
        st.markdown("Disease Prediction System to predict the risk of diabetes, heart disease, or Parkinson's based on your health data.")
        st.markdown("🔍 Log in and navigate to the Disease Prediction tab to get started.")

# Profile page (Login/Register)
elif menu == "👤 Profile":
    st.markdown("## 🔐 Login / Register")
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        login_user = st.text_input("👤 Username", key="login_user")
        login_pass = st.text_input("🔒 Password", type="password", key="login_pass")
        if st.button("Login"):
            users = load_users()
            if login_user in users and users[login_user] == hash_password(login_pass):
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid username or password.")
    
    with tab2:
        st.markdown("### Create a New Account")
        new_user = st.text_input("👤 Choose Username", key="register_user")
        new_pass = st.text_input("🔒 Choose Password", type="password", key="register_pass")
        if st.button("Register"):
            users = load_users()
            if new_user in users:
                st.warning("⚠️ Username already exists.")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.success("✅ Registration successful! You can now log in.")

# Disease prediction page
elif menu == "🔬 Disease Prediction":
    if st.session_state.logged_in:
        st.markdown("## 🧠 Disease Prediction Tool")
        st.markdown("Select a disease and enter your health data to assess risk.")
        disease = st.sidebar.radio("Select Disease", ["Diabetes", "Heart Disease", "Parkinson's"], key="disease_select")
        
        if disease == "Diabetes":
            show_diabetes_page()
        elif disease == "Heart Disease":
            show_heart_disease_page()
        elif disease == "Parkinson's":
            show_parkinsons_page()
    else:
        st.warning("⚠️ Please log in to use the prediction tool.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: gray;'>© 2025 Disease Prediction System • Built with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)