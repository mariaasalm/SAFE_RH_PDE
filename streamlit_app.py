

import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
        host='mysql.hostinger.com',
        user='u458377734_maria',
        password= 'Mscs2017',
        database= 'u458377734_icu_bvh_paeds'
        )
        if conn.is_connected():
            st.success("Connected to the database!")
    except Error as e:
        st.error(f"Failed to connect to the database. Error: {str(e)}")
    finally:
        if conn.is_connected():
            conn.close()

st.title("Database Connection Test")
connect_to_database()
