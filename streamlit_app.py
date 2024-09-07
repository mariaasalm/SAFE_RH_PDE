
import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import style_css as css
import add_patients as pt
# import plotly as px


# Adding custom CSS
css.add_custom_css()
# Function to connect to the database



def add_vitals():
    st.title("Enter Patient Vitals")

    patients = pt.fetch_patient_names()
    patient_names = [name[1] for name in patients]
    patient_ids = [name[0] for name in patients]

    # Dropdown to select patient
    selected_patient = st.selectbox("Select Patient", patient_names)
    selected_patient_id = patient_ids[patient_names.index(selected_patient)]

    # Form for vitals entry
    with st.form(key='vitals_form'):
        time = st.time_input("Time")
        date = st.date_input("Date")
        hr = st.text_input("Heart Rate (HR)")
        rr = st.text_input("Respiratory Rate (RR)")
        systolic = st.text_input("Systolic Blood Pressure")
        diastolic = st.text_input("Diastolic Blood Pressure")
        temp = st.text_input("Temperature (Temp)")
        sp02 = st.text_input("SpO2")
        bsr = st.text_input("Blood Sugar Level (BSR)")
        remarks = st.text_area("Remarks")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            conn = pt.get_db_connection()
            cursor = conn.cursor()
            query = '''
            INSERT INTO tb_pat_vitals (P_ID, Time, V_Date, HR, RR, Systolic, Diastolic, Temp, SpO2, BSR, Remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (selected_patient_id, time, date, hr, rr, systolic, diastolic, temp, sp02, bsr, remarks))
            conn.commit()
            conn.close()
            st.success("Vitals added successfully!")


def view_patients():
    st.header("View Patients")
    conn = pt.get_db_connection()
    query = "SELECT * FROM tb_patient"
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df)

def view_vitals():
    st.header("View Vitals")
    conn = pt.get_db_connection()
    query = "SELECT * FROM tb_pat_vitals"
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df)

def plot_patient_data():
    st.header("Patient Data Visualization")
    conn = pt.get_db_connection()
    query = "SELECT * FROM tb_patient"
    df = pd.read_sql(query, conn)
    conn.close()

    # Example plot: Distribution of patient ages
    st.subheader("Distribution of Patient Ages")
    fig = plt.figure(figsize=(10, 6))
    plt.hist(df['P_Age'], bins=range(0, 100, 10), edgecolor='black')
    plt.xlabel('Age')
    plt.ylabel('Number of Patients')
    plt.title('Age Distribution of Patients')
    st.pyplot(fig)

    # Example plot: Gender distribution
    st.subheader("Gender Distribution")
    gender_counts = df['Gender'].value_counts()
    fig = px.pie(names=gender_counts.index, values=gender_counts.values, title='Gender Distribution')
    st.plotly_chart(fig)

def main():
    st.sidebar.title("SAFE-RH Pediatric Module")
    option = st.sidebar.radio("Select Page", ["Add Patients", "Add Vitals", "View Patients", "View Vitals", "Patient Data Visualization"])

    if option == "Add Patients":
        pt.add_patient()
    elif option == "Add Vitals":
        add_vitals()
    elif option == "View Patients":
        view_patients()
    elif option == "View Vitals":
        view_vitals()
    # elif option == "Patient Data Visualization":
    #     plot_patient_data()

if __name__ == '__main__':
    main()
