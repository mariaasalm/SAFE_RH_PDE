# Custom CSS for styling
import streamlit as st
def add_custom_css():
    st.markdown("""
        <style>
        /* Center align the header */
        h1 {
            color: #4CAF50;
            text-align: center;
        }

        /* Customize input fields */
        input {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
        }

        /* Customize buttons */
        button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }

        /* Change background color */
        .stApp {
            background-color: #F0F8FF;
        }
        </style>
    """, unsafe_allow_html=True)