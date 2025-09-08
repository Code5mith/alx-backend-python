import mysql.connector
from dotenv import load_dotenv
import os

def stream_users_in_batches(batch_size):
    """Yield rows from user_data in batches of batch_size."""
    load_dotenv()
    conn = None
    cursor = None
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            user=os.getenv("USER"),
            host=os.getenv("HOST"),
            password=os.getenv("KEY"),
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Fetch rows in batches
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def batch_processing(batch_size):
    """Process batches to yield users over 25 years old."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
