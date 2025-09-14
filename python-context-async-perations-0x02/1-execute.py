import sqlite3

class ExecuteQuery():
    def __init__(self, db_name, age):
        self.db_name = db_name
        self.age = age 

    def __enter__(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE age > {self.age}")
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # connection is cleaned already
        pass