import mysql.connector
from dotenv import load_dotenv
import os

def stream_users():
    """Stream rows from user_data table one by one using a generator."""
    load_dotenv()
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            user=os.getenv("USER"),
            host=os.getenv("HOST"),
            password=os.getenv("KEY"),
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all rows
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Yield rows one by one
        for row in cursor:
            yield row
            
    finally:
        cursor.close()
        conn.close()