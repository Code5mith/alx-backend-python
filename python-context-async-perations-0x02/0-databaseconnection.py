import sqlite3


class DB_CONNECTION():
    def __init__(self,db_name=":memory", query:str="") -> None:
        self.conn = None
        self.db_name = db_name
    def __enter__(self):

        print("Set up: Opening database connection...")
        try:
            self.conn = sqlite3.connect(self.db_name)
            # return value is assigned to the variable after 'as' in the 'with' statement.
            return self.conn
            
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None 
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        print("exited")
        return False
    
with DB_CONNECTION() as conn:
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users")
    