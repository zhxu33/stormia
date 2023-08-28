import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('host')
user = os.getenv('user')
passwd = os.getenv('passwd')
database = os.getenv('database')

db = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
)

mycursor = db.cursor()

try: 
    mycursor.execute("CREATE DATABASE " + database)
    print("Successfully built database")
except:
    print("Database found")

db = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
    database = database
)

mycursor = db.cursor()

try:
    mycursor.execute("CREATE TABLE User (tag VARCHAR(50) PRIMARY KEY, total int, start datetime, clocking bool)")
    print("Successfully created table")
except:
    print("Table found")