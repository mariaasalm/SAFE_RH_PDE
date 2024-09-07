# Function to fetch data from the database
def fetch_data():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_labs")
        rows = cursor.fetchall()
        connection.close()
        return rows
    return []

# Function to add a new entry to the database
def add_entry(lab_id, test_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tb_labs (Lab_ID, test_name) VALUES (%s, %s)",
            (lab_id, test_name)
        )
        connection.commit()
        connection.close()
        st.success("Entry added successfully!")

# Streamlit app interface
def main():
    st.title("Lab Tests Management")

    # Display existing entries
    st.subheader("Existing Lab Tests")
    data = fetch_data()
    if data:
        st.write(data)
    else:
        st.write("No data available.")

    # Add new entry form
    st.subheader("Add New Lab Test")
    with st.form(key='add_entry_form'):
        lab_id = st.number_input("Lab ID", min_value=1, max_value=1000)
        test_name = st.text_input("Test Name")
        submit_button = st.form_submit_button(label='Add Entry')
        
        if submit_button:
            if lab_id and test_name:
                add_entry(lab_id, test_name)
            else:
                st.error("Please provide both Lab ID and Test Name.")

if __name__ == "__main__":
    main()
