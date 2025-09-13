import mysql.connector
from dotenv import load_dotenv
import os

def stream_user_ages():
    """Yield user ages one by one from user_data table."""
    load_dotenv()
    conn = None
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            user=os.getenv("USER"),
            host=os.getenv("HOST"),
            password=os.getenv("KEY"),
            database="ALX_prodev"
        )
        cursor = conn.cursor()
        
        # Fetch ages one by one
        cursor.execute("SELECT age FROM user_data")
        for age in cursor:
            yield age[0]
            
    finally:
        if conn and conn.is_connected():
            conn.close()

def calculate_average_age():
    """Calculate average age using streamed ages."""
    total_age = 0
    count = 0
    # pause for every yeild call 
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    # Avoid division by zero
    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()