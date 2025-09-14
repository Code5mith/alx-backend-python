import sqlite3

class ExecuteQuery():
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params

    def __enter__(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(self.query, self.params)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # connection already cleaned
        pass


with ExecuteQuery(
        db_name=':memory:',
        query="SELECT name, age FROM users WHERE age > ?",
        params=(25,)
    ) as results:
        if results:
            print("Query results:", results)
        else:
            print("No results returned.")