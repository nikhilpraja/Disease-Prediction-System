import streamlit as st
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Send email notification
def send_email(to_email, username):
    sender_email = "prajapatinikhil201@gmail.com"  # Replace with your email
    sender_password = "Nikhil@201"  # Replace with your app-specific password
    
    subject = "Welcome to Our Platform!"
    body = f"Dear {username},\n\nThank you for registering with us!\nYour account has been successfully created.\n\nBest regards,\nThe Team"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Register user
def register_user(username, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                 (username, email, hash_password(password)))
        conn.commit()
        send_email(email, username)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Login user
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == hash_password(password):
        return True
    return False

# Main Streamlit app
def main():
    st.title("User Authentication System")
    
    # Initialize database
    init_db()
    
    # Session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
    
    # Menu
    menu = ["Login", "Register", "Home"]
    if st.session_state.logged_in:
        menu.append("Logout")
    
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Register":
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if not new_username or not new_email or not new_password:
                    st.error("All fields are required")
                elif not is_valid_email(new_email):
                    st.error("Invalid email format")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    if register_user(new_username, new_email, new_password):
                        st.success("Registration successful! Email notification sent.")
                        st.info("Please login to continue")
                    else:
                        st.error("Username or email already exists")
    
    elif choice == "Login":
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username}!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
    
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.experimental_rerun()
    
    elif choice == "Home" and st.session_state.logged_in:
        st.subheader(f"Welcome {st.session_state.username}!")
        st.write("This is your dashboard.")
    
    else:
        st.write("Please login or register to continue.")

if __name__ == '__main__':
    main()