import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            query = args[0]
            print(f"Executing SQL query: '{query}' {datetime.today()}")
        else:
            query = kwargs.get('query')
            if query:
                print(f"Executing SQL query: '{datetime.today()}'")

        results = func(*args, **kwargs)
        return results

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


users = fetch_all_users(query="SELECT * FROM users")
print("\nQuery results:")
print(users)
