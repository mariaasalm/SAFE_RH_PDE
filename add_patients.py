# Add patient form
import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
def get_db_connection():
    return mysql.connector.connect(
        # Replace these with your actual credentials and settings
    host="id-dci-web1158.main-hosting.eu",
    user="u458377734_maria",
    password="Mscs2017",
    database="u458377734_icu_bvh_paeds"
    )

# Fetch some data from the database
def fetch_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_patient")
    data = cursor.fetchall()
    conn.close()
    return data

# Streamlit app
def main():
    st.title("Test Database Connection")

    # Fetch and display data
    data = fetch_data()
    if data:
        for row in data:
            st.write(row)
    else:
        st.write("No data found in the tb_patient table.")

if __name__ == "__main__":
    main()
