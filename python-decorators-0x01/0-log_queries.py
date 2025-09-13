import sqlite3
import functools

# Correct decorator to log SQL queries
# It takes the original function as an argument.
def log_queries(func):
    # This wrapper function will replace the original function.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # We need to access the query argument *before* the function runs.
        # Assuming the query is always the first positional argument.
        if args:
            query = args[0]
            print(f"Executing SQL query: '{query}'")
        else:
            # Handle cases where the query might be passed as a keyword argument
            query = kwargs.get('query')
            if query:
                print(f"Executing SQL query: '{query}'")

        # Now, execute the original function and get its result.
        # We pass along all original arguments and keyword arguments.
        results = func(*args, **kwargs)
        # The function has finished, so we can return its results.
        return results

    return wrapper

@log_queries
def fetch_all_users(query):
    # Note: In a real app, you would use a connection pool and
    # parameterize your query to prevent SQL injection.
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage to demonstrate the decorator
if __name__ == "__main__":
    # Create a dummy database for the example
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
    conn.commit()
    conn.close()

    # The decorator's logic will run before this function's code
    users = fetch_all_users(query="SELECT * FROM users")
    print("\nQuery results:")
    print(users)
