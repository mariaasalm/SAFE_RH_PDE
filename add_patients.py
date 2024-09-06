# Add patient form
import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
def get_db_connection():
    return mysql.connector.connect(
        # Replace these with your actual credentials and settings
        host="localhost",
        user="root",
        password="",
        database="id19588020_icu_bvh_paeds"
    )
def add_patient():
    st.header("Add Patients")
    with st.form(key='patient_form'):
        name = st.text_input("Name")
        reg = st.number_input("Registration No", min_value=0)
        weight = st.number_input("Weight (kg)", min_value=0.0)
        address = st.text_input("Address")
        age = st.number_input("Age", min_value=0)
        diagnosis = st.text_input("Diagnosis")
        duration_days = st.number_input("Duration (days)", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female"])
        remarks = st.text_area("Remarks")
        added_by = st.text_input("Added By")  # New field

        # Calculate the end date based on duration in days
        end_date = datetime.now() + timedelta(days=duration_days)

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = '''
            INSERT INTO tb_patient (P_Name, P_Reg, P_Weight, P_Address, P_Age, Diagnosis, Duration, Gender, Remarks, edited_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (name, reg, weight, address, age, diagnosis, end_date, gender, remarks, added_by))
            conn.commit()
            conn.close()
            st.success("Patient added successfully!")

# Fetch patient names from the database
def fetch_patient_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT P_ID, P_Name FROM tb_patient")
    patients = cursor.fetchall()
    conn.close()
    return patients

