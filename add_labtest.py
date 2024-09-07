import streamlit as st
import mysql.connector
import pandas as pd
def create_connection():
       return mysql.connector.connect(
        # Replace these with your actual credentials and settings
    host="id-dci-web1158.main-hosting.eu",
    user="u458377734_maria",
    password="Mscs2017",
    database="u458377734_icu_bvh_paeds"
    )

# Fetch all lab tests from the database
def fetch_data():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_labs")
        rows = cursor.fetchall()
        connection.close()
        return rows
    return []

# Add a new lab test entry to the database
def add_entry( test_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tb_labs (test_name) VALUES ( %s)",
            (test_name)
        )
        connection.commit()
        connection.close()
        st.success(f"Lab test '{test_name}' added successfully!")

# Streamlit app interface
def main():
    # st.title("Lab Tests Management")

    # Tabs for multiple sections
    tab1, tab2, tab3 = st.tabs(["Add Lab Test", "View Tests", "Reports"])

    # Tab 1: Add Lab Test
    with tab1:
        st.header("Add New Lab Test")
        
        # Fetch existing lab tests for dropdown display
        # lab_tests = fetch_data()
        # test_names = [test['test_name'] for test in lab_tests]
        
        # Form for adding a new lab test
        with st.form(key='add_entry_form'):
            # lab_id = st.number_input("Lab ID", min_value=1, max_value=1000)
            test_name = st.text_input("Test Name")
            
            # Show existing tests in dropdown for reference
            # st.selectbox("Existing Lab Tests", options=test_names, index=0 if test_names else None)
            
            submit_button = st.form_submit_button(label='Add Entry')
            
            if submit_button:
                if test_name:
                    add_entry(test_name)
                else:
                    st.error("Please provide both Lab ID and Test Name.")

    # Tab 2: View Lab Tests
    with tab2:
        st.subheader("Existing Lab Tests")

        # Fetch existing lab test data
        data = fetch_data()
        # Add a search bar to filter results
        search_query = st.text_input("Search Lab Tests", value="", help="Enter the lab test name or part of it to search.")
        
        # Filter the results based on the search query
        if search_query:
            filtered_data = [lab for lab in data if search_query.lower() in lab['test_name'].lower()]
        else:
            filtered_data = data

        # Display filtered data in a table
        if filtered_data:
            df = pd.DataFrame(filtered_data)
            st.dataframe(df)
        else:
            st.write("No test found.")




    # Tab 3: Reports
    with tab3:
        st.header("Reports")
        st.write("This tab displays patient reports and graphs.")
        # Add charts, graphs, etc.

if __name__ == "__main__":
    main()
   

if __name__ == "__main__":


    main()
