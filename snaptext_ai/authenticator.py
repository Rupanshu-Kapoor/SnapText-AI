import firebase_admin
from firebase_admin import credentials
import streamlit as st
from pathlib import Path
import pyrebase
import json

credential_json_path = Path("../handwritting-recognisation-firebase-adminsdk-dp7g7-36ff22e7df.json")

firebase_config = {
  "apiKey": "AIzaSyBuB-bS412UJN5jaW8JL7nqJR0hFfbR1o4",
  "authDomain": "handwritting-recognisation.firebaseapp.com",
  "projectId": "handwritting-recognisation",
  "storageBucket": "handwritting-recognisation.appspot.com",
  "messagingSenderId": "804287642629",
  "appId": "1:804287642629:web:94cde1a630ba483fe0b06c",
  "measurementId": "G-LS6BFGJZ3Q",
  "databaseURL" : ""
}

# initialize firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(credential_json_path)
    firebase_admin.initialize_app(cred)

    firebase = pyrebase.initialize_app(firebase_config)
    firebase_initialized = True
else:
    firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

# initialize Firestore
# db = firebase.database()


def sign_up(name, email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        update_user_profile(user["idToken"], name)
        st.success("Account created successfully!")
    except Exception as e:
        error_message = json.loads(e.args[1])["error"]["message"]
        st.error(f"Failed to create account: {error_message}")


def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("Signed in successfully!")
        st.session_state['user'] = user
        st.session_state['email'] = email
        st.session_state["id_token"] = user["idToken"]
        st.experimental_rerun()
    except Exception as e:
        error_message = json.loads(e.args[1])["error"]["message"]
        st.error(f"Failed to sign in: {error_message}")
        
def sign_out():
    del st.session_state['user']
    del st.session_state['email']
    st.success("Signed out successfully!")
    st.experimental_rerun()
    

def forgot_password(email):
    try:
        auth.send_password_reset_email(email)
        st.success("Password reset link sent!")

    except Exception as e:
        error_message = json.loads(e.args[1])["error"]["message"]
        st.error(f"Failed to send password reset link: {error_message}")


def return_to_login():
    if st.button("Return to Login"):
        st.session_state["forgot_password"] = False
        del st.session_state["forgot_password"]


def update_user_profile(id_token, display_name):
    auth.update_profile(id_token, display_name = display_name)
    


st.title("SnapText-AI Login")

if 'user' in st.session_state:
    account_info = auth.get_account_info(st.session_state["id_token"])
    st.write(f"Signed in as: {account_info['users'][0].get('displayName', account_info['users'][0].get('email', 'Unknown'))}")
    st.write(account_info)
    if st.button("Sign Out"):
        sign_out()

elif "forgot_password" in st.session_state:
    email = st.text_input("Email", placeholder="Enter your email", key="forgot_email")
    reset_col, return_to_login_col = st.columns([7,2])
    with reset_col:
        if st.button("Send Reset Link"):
            forgot_password(email)
    with return_to_login_col:
        if st.button("Return to Login"):
            st.session_state["forgot_password"] = False
            del st.session_state["forgot_password"]
            st.experimental_rerun()
else:
    choice = st.selectbox("Choose action", ["Sign In", "Sign Up"])
    if choice == "Sign Up":
            name = st.text_input("Name", placeholder="Enter your name", key="signup_name")
            email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="********", key="signup_password")
            
    elif choice == "Sign In":
        email = st.text_input("Email", placeholder="Enter your email", key="signin_email")
        password = st.text_input("Password", type="password", placeholder="********", key="signin_password")


    login_col, forgot_pass_col = st.columns([7,2])
    with login_col:
        if st.button(choice):
            if choice == "Sign Up":
                sign_up(name, email, password)

            elif choice == "Sign In":
                user = sign_in(email, password)
        
    with forgot_pass_col:
        if st.button("Forgot Password"):
            st.session_state["forgot_password"] = True
            st.experimental_rerun()

           
