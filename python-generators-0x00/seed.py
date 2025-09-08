import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os 
import faker 
import pandas as pd
import random

load_dotenv()

def connect_db():
  conn = None
  try:
    conn = mysql.connector.connect(user=os.getenv("USER"),
                                  host=os.getenv("HOST"),
                                  password=os.getenv("KEY"),
                                  database='Alx_Air_BnB_DB')
    yield conn 
    
  except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access Denied Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)

  # finally:

  #   if conn and conn.is_connected():
  #       conn.close()


TABLES = {}

factory = faker.Faker()

# Generator Obj
Connect_DB = connect_db()

TABLES['user_data'] = (
"""
    CREATE TABLE IF NOT EXISTS `user_data` (
    `user_id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `age` INT(11) NOT NULL
    )  ENGINE=InnoDB
"""
  )

def create_database(DB_Connection):
  cursor = DB_Connection.cursor()
  print("Creating DB")
  yield {
    
    cursor.execute(
    """ 
      CREATE DATABASE IF NOT EXISTS `ALX_prodev`
    """
  )
}
  DB_Connection.close()
  print(DB_Connection.is_connected())

def connect_to_prodev(DB_Connection):
  cursor = DB_Connection.cursor()
  print("Connecting to DB")
  yield cursor.execute(
    """
      USE `ALX_prodev`
    """
  )

def create_table(DB_Connection, Return_Connection:bool = False): 

  cursor = DB_Connection.cursor()

  # Create DB
  next(create_database(DB_Connection=DB_Connection))

  cursor.execute(
    """
      SHOW DATABASES
    """
  )

  DB_LIST = cursor.fetchall()


  print(DB_LIST[0][0])

  for db in DB_LIST:
    if db[0] == "ALX_prodev":
      # Connect to DB
      next(connect_to_prodev(DB_Connection=DB_Connection))
      # Create user_date
      cursor.execute(TABLES["user_data"])
    else:
      print("Db not found")
      
    DB_Connection.close()
  

def insert_data(DB_Connection):

  df = pd.read_csv("sample_data.csv") 

  cursor = DB_Connection.cursor()

  cursor.execute(
    """
      SHOW DATABASES
    """
  )

  DB_LIST = cursor.fetchall()

  for db in DB_LIST:
    if db[0] == "ALX_prodev":
      # Connect to DB
      next(connect_to_prodev(DB_Connection=DB_Connection))
      
      cursor.execute(
        """ 
          SHOW TABLES
        """
      )
      results = cursor.fetchall()

      for result in results:

        if result[0] == "user_data":

          print("Table found!")

          for x in range(5):
            index = random.randint(0,len(df)) 
            cursor.execute(
                """
                  INSERT INTO `user_data` (name, email, age)
                  VALUES (%s, %s, %s);
                """,
                (df["name"][index], df["email"][index], int(df["age"][index]))
              )
          
            DB_Connection.commit()

        else:
          print("*** Table not found!")
          create_table(DB_Connection=DB_Connection)
          next(connect_to_prodev(DB_Connection=DB_Connection))
          cursor.execute(
              """
                INSERT INTO `user_data` (name, email, age)
                VALUES (%s, %s, %s);
              """,
              (factory.name(), factory.email(), factory.random_number(2))
            )

          DB_Connection.commit()

  DB_Connection.close()
  print("Db Connection :", DB_Connection.is_connected())

insert_data(next(connect_db()))

