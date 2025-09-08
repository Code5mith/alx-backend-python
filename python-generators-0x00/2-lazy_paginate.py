import mysql.connector
from dotenv import load_dotenv
import os

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    load_dotenv()
    try:
        conn = mysql.connector.connect(
            user=os.getenv("USER"),
            host=os.getenv("HOST"),
            password=os.getenv("KEY"),
            database="ALX_prodev"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        raise

def paginate_users(page_size, offset):
    """Fetch a page of users from user_data."""
    conn = connect_to_prodev()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()
