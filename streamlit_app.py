import pymysql

db_config = {
    'host': 'u458377734_icu_bvh_paeds.hostinger.com',
    'user': 'u458377734_maria',
    'password': 'Mscs2017',
    'database': 'u458377734_icu_bvh_paeds'
}

def test_connection():
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            st.write(f"Connected to database: {db_name[0]}")
        st.success("Successfully connected to the database!")
    except pymysql.MySQLError as e:
        st.error(f"Error: {e}")
    finally:
        if conn:
            conn.close()
