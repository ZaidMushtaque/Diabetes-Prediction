import streamlit as st
import pandas as pd
import pickle

from database import add_user, login_user

# Load ML model
model = pickle.load(open('diabetes_model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

# ---------------- SESSION STATE ----------------

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""

# ---------------- SIDEBAR ----------------

if not st.session_state.logged_in:
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)
else:
    st.sidebar.write(f"👤 Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    choice = "Home"

# ---------------- SIGNUP ----------------

if not st.session_state.logged_in and choice == "Signup":

    st.title("Create Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')

    if st.button("Signup"):
        add_user(new_user, new_password)
        st.success("✅ Account Created Successfully")
        st.info("Go to Login Page")

# ---------------- LOGIN ----------------

elif not st.session_state.logged_in and choice == "Login":

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        result = login_user(username, password)

        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ---------------- PREDICTOR (shown after login) ----------------

elif st.session_state.logged_in:

    st.success(f"Welcome {st.session_state.username}")
    st.title("AAC Diabetes Predictor")

    preg     = st.number_input('Pregnancies', 0, 20, 1)
    glucose  = st.number_input('Glucose', 0, 300, 120)
    bp       = st.number_input('Blood Pressure', 0, 150, 70)
    skin     = st.number_input('Skin Thickness', 0, 100, 20)
    insulin  = st.number_input('Insulin', 0, 900, 80)
    bmi      = st.number_input('BMI', 0.0, 70.0, 25.0)
    dpf      = st.number_input('Diabetes Pedigree Function', 0.0, 3.0, 0.5)
    age      = st.number_input('Age', 1, 100, 30)

    if st.button('Predict'):

        input_data = pd.DataFrame({
            'Pregnancies':              [preg],
            'Glucose':                  [glucose],
            'BloodPressure':            [bp],
            'SkinThickness':            [skin],
            'Insulin':                  [insulin],
            'BMI':                      [bmi],
            'DiabetesPedigreeFunction': [dpf],
            'Age':                      [age]
        })

        input_data = input_data.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("⚠️ High Risk of Diabetes")
        else:
            st.success("✅ Low Risk of Diabetes")
