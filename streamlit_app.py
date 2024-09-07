
import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import style_css as css
import plotly as px
import add_labtest as lt
import add_patients as pt
import add_med as md

# Adding custom CSS
css.add_custom_css()
# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        # Replace these with your actual credentials and settings
    host="id-dci-web1158.main-hosting.eu",
    user="u458377734_maria",
    password="Mscs2017",
    database="u458377734_icu_bvh_paeds"
    )

def add_patient():
    st.subheader("Add New Patient")
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
def view_patients():
    st.subheader("View Patients")
    conn = get_db_connection()
    query = "SELECT * FROM tb_patient"
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df)
def patient():
    st.header("Patient Core: Patients Management System")
    tab1, tab2, tab3 = st.tabs(["Add Patients","View Patients","Edit"])
    with tab1:
        add_patient()
    with tab2:
        view_patients()
# Fetch patient names from the database
def fetch_patient_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT P_ID, P_Name FROM tb_patient")
    patients = cursor.fetchall()
    conn.close()
    return patients



def add_vitals():
    # st.header("Vital Tracker: Patient Vitals Monitoring")

    patients = fetch_patient_names()
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
            conn = get_db_connection()
            cursor = conn.cursor()
            query = '''
            INSERT INTO tb_pat_vitals (P_ID, Time, V_Date, HR, RR, Systolic, Diastolic, Temp, SpO2, BSR, Remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (selected_patient_id, time, date, hr, rr, systolic, diastolic, temp, sp02, bsr, remarks))
            conn.commit()
            conn.close()
            st.success("Vitals added successfully!")




def view_vitals():
    st.subheader("View Patients Vitals")
    conn = get_db_connection()
    query = "SELECT * FROM tb_pat_vitals"
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df)

def vitals():
    st.header("Vital Tracker: Patient Vitals Management System")
    tab1, tab2, tab3 = st.tabs(["Add Vitals","View Vitals","Edit"])
    with tab1:
        add_vitals()
    with tab2:
        view_vitals()

def labs():
    st.header("Lab Tracker: Patient Lab Test Management System")
    tab1, tab2, tab3 = st.tabs(["Add Lab","View Labs","Edit"])
    with tab1:
        lt.add_entry()
    with tab2:
       lt.fetch_data


def plot_patient_data():
    st.subheader("Patient Data Visualization")
    conn = get_db_connection()
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
        # add_logo()
    st.sidebar.image('logo.jpg')

    st_image = """
    <style>
    .st-emotion-cache-1v0mbdj {
        position: relative;
        top: -10px;
        bottom: 50px; /* Adjust as needed */
        left: 0px; /* Adjust as needed */
        width: 100%; /* Ensure it stays within the sidebar width */
        padding: 10px; /* Optional: add padding */
    } 
    </style>
    """
    st.markdown(st_image, unsafe_allow_html=True)
    st.sidebar.subheader("PediaTrak – A Pediatric ICU Data Collection and Monitoring System")

    option = st.sidebar.radio("Menu", ["Patient Core", "Vital Tracker" ,"Lab Tracker","Med Tracker"])

    if option == "Patient Core":
        patient()
    elif option == "Vital Tracker":
        vitals()
    elif option == "Lab Tracker":
        lt.main()
    elif option == "Med Tracker":
        md.main()
    
  
  
if __name__ == '__main__':
    main()
    # lt.main()


