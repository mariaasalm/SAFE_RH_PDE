import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def connect_to_database():
    try:
        st.write("Attempting to connect to the database...")
        conn = mysql.connector.connect(
            host='taci.com.pk',  # Make sure this host is correct
            user='u458377734_maria',
            password='Mscs2017',
            database='u458377734_icu_bvh_paeds',
            connection_timeout=10  # Set a timeout to avoid hanging
        )
        if conn.is_connected():
            st.success("Connected to the database!")
        else:
            st.error("Connection failed without exception.")
    except Error as e:
        st.error(f"Failed to connect to the database. Error: {str(e)}")
    finally:
        try:
            if conn.is_connected():
                conn.close()
                st.write("Connection closed.")
        except:
            st.write("Connection could not be established, no need to close.")

st.title("Database Connection Test")
connect_to_database()
