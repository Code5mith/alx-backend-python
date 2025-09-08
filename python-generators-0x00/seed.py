import mysql.connector
from mysql.connector import errorcode
import os
import uuid
import csv
import sys

# Replace with your MySQL credentials from .env
# This assumes your .env file is set up correctly
MYSQL_HOST = os.getenv("HOST")
MYSQL_USER = os.getenv("USER")
MYSQL_PASSWORD = os.getenv("KEY")
DATABASE_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def connect_db():
    """
    Connects to the MySQL database server and returns a connection object.
    
    Returns:
        mysql.connector.connection.MySQLConnection: The connection object if successful, None otherwise.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied: Check your user name or password.")
        else:
            print(f"Connection Error: {err}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """
    Connects to the ALX_prodev database and returns a connection object.
    
    Returns:
        mysql.connector.connection.MySQLConnection: The connection object if successful, None otherwise.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DATABASE_NAME}': {err}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist.
    """
    cursor = connection.cursor()
    try:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
            `user_id` VARCHAR(36) PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL UNIQUE,
            `age` INT NOT NULL
        ) ENGINE=InnoDB
        """
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{TABLE_NAME}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data_file_path):
    """
    Inserts data from a CSV file into the user_data table.
    """
    cursor = connection.cursor()
    try:
        insert_query = f"""
        INSERT INTO `{TABLE_NAME}` (user_id, name, email, age) 
        VALUES (%s, %s, %s, %s)
        """
        
        with open(data_file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            
            records_to_insert = []
            for row in reader:
                user_id = str(uuid.uuid4())
                name, email, age = row
                records_to_insert.append((user_id, name, email, int(age)))
        
            if records_to_insert:
                cursor.executemany(insert_query, records_to_insert)
                connection.commit()
                print("Data inserted successfully.")
            else:
                print("No data to insert.")

    except FileNotFoundError:
        print(f"Error: The file '{data_file_path}' was not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
