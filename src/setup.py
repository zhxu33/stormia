import mysql.connector
from info import *

db = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
)

mycursor = db.cursor()

def build():
    try: 
        mycursor.execute("CREATE DATABASE " + database)
        return "Successfully built database."
    except:
        return "Database already exists."
    
def drop():
    try: 
        mycursor.execute("DROP DATABASE " + database)
        return "Successfully deleted database."
    except:
        return "Database does not exist"