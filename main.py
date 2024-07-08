# -*- coding: utf-8 -*-
"""
Created on Sat Jun  15 01:02:34 2024

@author: aumvashi
"""
import pickle
import sqlite3
import bcrypt
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Function to create the database and users table
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        age INTEGER,
        gender TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user(username, password, full_name, email, age, gender):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute('''
    INSERT INTO users (username, password, full_name, email, age, gender)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, hashed_password, full_name, email, age, gender))
    conn.commit()
    conn.close()

# Function to validate login credentials
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT password FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user[0]):
            return True
        else:
            st.warning('Password does not match.')
    else:
        st.warning('Username not found.')
    return False

# Function to retrieve user details
def get_user_details():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT username, full_name, email, age, gender, password FROM users
    ''')
    users = c.fetchall()
    conn.close()
    return users

# Create the database and table
create_db()

# Function to display login form
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == 'admin' and password == 'root':
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["is_admin"] = True
            st.experimental_rerun()
        elif validate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["is_admin"] = False
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Function to display sign-up form
def signup():
    st.title("Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_username and new_password:
            add_user(new_username, new_password, full_name, email, age, gender)
            st.success("Account created successfully! Please log in.")
            st.experimental_rerun()
        else:
            st.error("Please fill in all required fields")

# Function to display logout button
def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["is_admin"] = False
        st.experimental_rerun()

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Sidebar navigation for login, sign-up, and predictions
with st.sidebar:
    nav = option_menu("Register", ["Login", "Sign Up", "Home"],
                      icons=["person", "person-plus", "house"],
                      menu_icon="cast", default_index=2)

if nav == "Login":
    login()
elif nav == "Sign Up":
    signup()
elif nav == "Home":
    if not st.session_state["logged_in"]:
        st.warning("Please log in to access this page")
    else:
        logout()

        # loading the saved models
        diabetes_model = pickle.load(open('C:/Users/aumva/OneDrive/Desktop/Prediction/saved-models/diabetes_model.sav', 'rb'))
        heart_disease_model = pickle.load(open('C:/Users/aumva/OneDrive/Desktop/Prediction/saved-models/heart_disease_model.sav', 'rb'))
        parkinsons_model = pickle.load(open('C:/Users/aumva/OneDrive/Desktop/Prediction/saved-models/parkinsons_model.sav', 'rb'))

        # sidebar for navigation
        with st.sidebar:
            selected = option_menu('Multiple Disease Prediction System',
                                   ['Diabetes Prediction',
                                    'Heart Disease Prediction',
                                    'Parkinsons Prediction'],
                                   menu_icon='hospital-fill',
                                   icons=['activity', 'heart', 'person'],
                                   default_index=0)

        # Diabetes Prediction Page
        if selected == 'Diabetes Prediction':
            # page title
            st.title('Diabetes Prediction using ML')
            # getting the input data from the user
            col1, col2, col3 = st.columns(3)

            with col1:
                Pregnancies = st.text_input('Number of Pregnancies')

            with col2:
                Glucose = st.text_input('Glucose Level')

            with col3:
                BloodPressure = st.text_input('Blood Pressure value')

            with col1:
                SkinThickness = st.text_input('Skin Thickness value')

            with col2:
                Insulin = st.text_input('Insulin Level')

            with col3:
                BMI = st.text_input('BMI value')

            with col1:
                DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

            with col2:
                Age = st.text_input('Age of the Person')

            # code for Prediction
            diab_diagnosis = ''

            # creating a button for Prediction
            if st.button('Diabetes Test Result'):
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                              BMI, DiabetesPedigreeFunction, Age]
                user_input = [float(x) for x in user_input]
                diab_prediction = diabetes_model.predict([user_input])
                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'

            st.success(diab_diagnosis)

        # Heart Disease Prediction Page
        if selected == 'Heart Disease Prediction':
            # page title
            st.title('Heart Disease Prediction using ML')

            col1, col2, col3 = st.columns(3)

            with col1:
                age = st.text_input('Age')

            with col2:
                sex = st.text_input('Sex')

            with col3:
                cp = st.text_input('Chest Pain types')

            with col1:
                trestbps = st.text_input('Resting Blood Pressure')

            with col2:
                chol = st.text_input('Serum Cholestoral in mg/dl')

            with col3:
                fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

            with col1:
                restecg = st.text_input('Resting Electrocardiographic results')

            with col2:
                thalach = st.text_input('Maximum Heart Rate achieved')

            with col3:
                exang = st.text_input('Exercise Induced Angina')

            with col1:
                oldpeak = st.text_input('ST depression induced by exercise')

            with col2:
                slope = st.text_input('Slope of the peak exercise ST segment')

            with col3:
                ca = st.text_input('Major vessels colored by flourosopy')

            with col1:
                thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

            # code for Prediction
            heart_diagnosis = ''

            # creating a button for Prediction
            if st.button('Heart Disease Test Result'):
                user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
                user_input = [float(x) for x in user_input]
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person has heart disease'
                else:
                    heart_diagnosis = 'The person does not have heart disease'

            st.success(heart_diagnosis)

        # Parkinson's Prediction Page
        if selected == "Parkinsons Prediction":
            # page title
            st.title("Parkinson's Disease Prediction using ML")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                fo = st.text_input('MDVP:Fo(Hz)')

            with col2:
                fhi = st.text_input('MDVP:Fhi(Hz)')

            with col3:
                flo = st.text_input('MDVP:Flo(Hz)')

            with col4:
                Jitter_percent = st.text_input('MDVP:Jitter(%)')

            with col5:
                Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

            with col1:
                RAP = st.text_input('MDVP:RAP')

            with col2:
                PPQ = st.text_input('MDVP:PPQ')

            with col3:
                DDP = st.text_input('Jitter:DDP')

            with col4:
                Shimmer = st.text_input('MDVP:Shimmer')

            with col5:
                Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

            with col1:
                APQ3 = st.text_input('Shimmer:APQ3')

            with col2:
                APQ5 = st.text_input('Shimmer:APQ5')

            with col3:
                APQ = st.text_input('MDVP:APQ')

            with col4:
                DDA = st.text_input('Shimmer:DDA')

            with col5:
                NHR = st.text_input('NHR')

            with col1:
                HNR = st.text_input('HNR')

            with col2:
                RPDE = st.text_input('RPDE')

            with col3:
                DFA = st.text_input('DFA')

            with col4:
                spread1 = st.text_input('spread1')

            with col5:
                spread2 = st.text_input('spread2')

            with col1:
                D2 = st.text_input('D2')

            with col2:
                PPE = st.text_input('PPE')

            # code for Prediction
            parkinsons_diagnosis = ''

            # creating a button for Prediction    
            if st.button("Parkinson's Test Result"):
                user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                              RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                              APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
                user_input = [float(x) for x in user_input]
                parkinsons_prediction = parkinsons_model.predict([user_input])
                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "The person has Parkinson's disease"
                else:
                    parkinsons_diagnosis = "The person does not have Parkinson's disease"

            st.success(parkinsons_diagnosis)

# Admin Page
def admin_page():
    st.title("Admin Page")
    st.write("Welcome to the admin page. Here you can manage users.")

    users = get_user_details()
    st.write("### User Details")
    for user in users:
        st.write(f"**Username:** {user[0]}")
        st.write(f"**Full Name:** {user[1]}")
        st.write(f"**Email:** {user[2]}")
        st.write(f"**Age:** {user[3]}")
        st.write(f"**Gender:** {user[4]}")
        st.write(f"**Password:** {user[5]}")
        st.write("---")

# Check if user is admin
if st.session_state["is_admin"]:
    admin_page()
