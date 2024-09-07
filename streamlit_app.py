import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='u458377734_icu_bvh_paeds.hostinger.com',
            user='u458377734_maria',
            password= 'Mscs2017',
            database= 'u458377734_icu_bvh_paeds'
        )
        if conn.is_connected():
            return True
    except Error as e:
        return False

# Main Streamlit App
def main():
    st.title("Database Connection Test")

    # Check database connection
    if connect_to_database():
        st.success("Database connected successfully!")
    else:
        st.error("Failed to connect to the database.")

if __name__ == '__main__':
    main()

