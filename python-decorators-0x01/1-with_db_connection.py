import sqlite3 
import mysql.connector
import functools

# Decorator to handle opening and closing database connections.
def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish the connection
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="app_user",
                password="SecureP@ssw0rd123",
                database="airbnb_db"
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return Exception 

        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("Database connection closed.")

    return wrapper


@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)

print(user)