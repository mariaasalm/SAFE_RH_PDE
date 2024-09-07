import streamlit as st
import mysql.connector
import pandas as pd

# Database connection setup
def create_connection():
    return mysql.connector.connect(
        # Replace these with your actual credentials and settings
    host="id-dci-web1158.main-hosting.eu",
    user="u458377734_maria",
    password="Mscs2017",
    database="u458377734_icu_bvh_paeds"
    )

# Fetch all medicines from the database
def fetch_medicines():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_medicines")
        rows = cursor.fetchall()
        connection.close()
        return rows
    return []

# Add a new medicine entry to the database
def add_medicine( med_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tb_medicines ( med_name) VALUES ( %s)",
            ( med_name)
        )
        connection.commit()
        connection.close()
        st.success(f"Medicine '{med_name}' added successfully!")

# Streamlit app interface
def main():
    # st.title("Medicine Management")

    # Tabs for multiple sections
    tab1, tab2, tab3 = st.tabs(["Add Medicine", "View Medicines", "Reports"])

    # Tab 1: Add Medicine
    with tab1:
        st.header("Add New Medicine")

        # Fetch existing medicines for dropdown display
        medicines = fetch_medicines()
        med_names = [med['med_name'] for med in medicines]

        # Form for adding a new medicine
        with st.form(key='add_medicine_form'):
            # m_id = st.number_input("Medicine ID", min_value=1, max_value=1000)
            med_name = st.text_input("Medicine Name")
            
            # Show existing medicines in dropdown for reference
            st.selectbox("Existing Medicines", options=med_names, index=0 if med_names else None)
            
            submit_button = st.form_submit_button(label='Add Medicine')
            
            if submit_button:
                if med_name:
                    add_medicine( med_name)
                else:
                    st.error("Please provide both Medicine ID and Medicine Name.")

    # Tab 2: View Medicines with Search
    with tab2:
        st.subheader("Existing Medicines")
        
        # Fetch existing medicines
        data = fetch_medicines()

        # Add a search bar to filter results
        search_query = st.text_input("Search Medicines", value="", help="Enter the medicine name or part of it to search.")
        
        # Filter the results based on the search query
        if search_query:
            filtered_data = [med for med in data if search_query.lower() in med['med_name'].lower()]
        else:
            filtered_data = data

        # Display filtered data in a table
        if filtered_data:
            df = pd.DataFrame(filtered_data)
            st.dataframe(df)
        else:
            st.write("No medicines found.")

    # Tab 3: Reports
    with tab3:
        st.header("Reports")
        st.write("This tab displays reports and statistics related to medicines.")
        # Add charts, graphs, etc.

if __name__ == "__main__":
    main()
