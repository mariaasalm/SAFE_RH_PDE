import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import config as con

# Fetch patient names from the tb_patient table
def fetch_patient_names():
    conn = con.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT P_ID, P_Name FROM tb_patient")
    patients = cursor.fetchall()
    conn.close()
    return patients

# Add new patient vitals to the tb_pat_vitals table
def add_vitals(p_id, time, v_date, hr, rr, systolic, diastolic, temp, spo2, bsr, remarks):
    conn = con.get_db_connection()
    cursor = conn.cursor()
    query = '''
    INSERT INTO tb_pat_vitals (P_ID, Time, V_Date, HR, RR, Systolic, Diastolic, Temp, SpO2, BSR, Remarks)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (p_id, time, v_date, hr, rr, systolic, diastolic, temp, spo2, bsr, remarks))
    conn.commit()
    conn.close()

# Form for adding patient vitals with validation
def add_vitals_form():
    st.header("Add Patient Vitals")
    # Fetch existing patients for dropdown
    patients = fetch_patient_names()
    patient_dict = {patient['P_Name']: patient['P_ID'] for patient in patients}
    patient_name = st.selectbox("Select Patient", options=list(patient_dict.keys()))
    p_id = patient_dict[patient_name]
    with st.form(key='vitals_form'):
        # Allow the user to input any time and date within one month ago and current
        time = st.time_input("Time HH:MM:")
        v_date = st.date_input("Date", value=datetime.now().date())
    # Heart Rate and Respiratory Rate (No decimals allowed)
        hr = st.text_input("Heart Rate (HR)", value="").strip()
        rr = st.text_input("Respiratory Rate (RR)", value="").strip()

        # Blood Pressure (Systolic/Diastolic validation)
        systolic = st.number_input("Systolic Blood Pressure (BP)", min_value=60, max_value=220)
        diastolic = st.number_input("Diastolic Blood Pressure (BP)", min_value=20, max_value=120)

        # Temperature
        temp = st.number_input("Temperature (Temp)", min_value=90, max_value=106)

        # SpO2
        spo2 = st.number_input("Oxygen Saturation (SpO2)", min_value=50, max_value=100)

        # Blood Sugar Random (BSR)
        bsr = st.text_input("Blood Sugar Random (BSR)", value="").strip()

        # Remarks
        remarks = st.text_area("Remarks")

        submit_button = st.form_submit_button(label="Add Vitals")

        # Validation for inputs
        if submit_button:
            valid = True
            # HR and RR must be integers (not decimals)
            if not hr.isdigit():
                st.error("Heart Rate (HR) should be a whole number (no decimals).")
                valid = False
            if not rr.isdigit():
                st.error("Respiratory Rate (RR) should be a whole number (no decimals).")
                valid = False

            # Difference between Systolic and Diastolic must be within the range 25-50
            if not (25 <= (systolic - diastolic) <= 50):
                st.error("The difference between Systolic and Diastolic BP should be between 25 and 50.")
                valid = False

            # Proceed with database insertion if all validations pass
            if valid:
                add_vitals(p_id, time, v_date, hr, rr, systolic, diastolic, temp, spo2, bsr, remarks)
                st.success(f"Vitals for '{patient_name}' added successfully!")
            else:
                st.error("Please correct the errors before submitting.")
# Fetch vitals data from the tb_pat_vitals table
def fetch_vitals():
    conn = con.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
    SELECT v.V_ID, p.P_Name, v.Time, v.V_Date, v.HR, v.RR, v.Systolic, v.Diastolic, v.Temp, v.SpO2, v.BSR, v.Remarks 
    FROM tb_pat_vitals v 
    JOIN tb_patient p ON v.P_ID = p.P_ID
    ''')
    vitals = cursor.fetchall()
    conn.close()
    return vitals

# Display vitals data in a table
def view_vitals():
    st.header("View Patient Vitals")
    
    # Fetch vitals data
    vitals_data = fetch_vitals()

    if vitals_data:
        df = pd.DataFrame(vitals_data)
        st.dataframe(df)
    else:
        st.write("No vitals data found.")

# Main function to render the Streamlit app
def main():
    st.title("Patient Vitals Management System")
    
    # Tabs for adding and viewing vitals
    tab1, tab2 = st.tabs(["Add Vitals", "View Vitals"])

    with tab1:
        add_vitals_form()

    with tab2:
        view_vitals()

if __name__ == "__main__":
    main()
