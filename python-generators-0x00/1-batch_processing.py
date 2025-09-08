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
        
        print(f"Fetching user_data in batches of {batch_size}")
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Yield batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            print(f"Yielding batch of {len(batch)} users")
            yield batch
            
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed")

def batch_processing(batch_size):
    """Yield users over 25 years old from batches."""
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing batch of {len(batch)} users")
        for user in batch:
            if user['age'] > 25:
                print(f"Yielding user: {user['name']}, age {user['age']}")
                yield user