import mysql.connector
from datetime import datetime
import time

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd="123Rockey30$",
    database = "Stormia"
    )

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE User (tag VARCHAR(50) PRIMARY KEY, total int, start datetime, clocking bool)")
# mycursor.execute("DROP TABLE User")

def resume(userTag):
    mycursor.execute("UPDATE User SET clocking = %s, start = %s WHERE Tag = %s", (True, datetime.now(), userTag))
    db.commit()

def pause(userTag):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    total = (int) (result[1] + (datetime.now()-result[2]).total_seconds())
    mycursor.execute("UPDATE User SET total = %s, clocking = %s WHERE Tag = %s AND clocking = %s", (total, False, userTag, True))
    db.commit()

def insert(userTag):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if(str(result) == "None"):
        mycursor.execute("INSERT INTO User (tag, total, start, clocking) VALUES (%s,%s,%s,%s)", (userTag, 0, datetime.now(), False))
        db.commit()
        return True
    return False

def drop(userTag):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if(str(result) != "None"):
        mycursor.execute("DELETE FROM User WHERE tag = %s", [userTag])
        db.commit()
        return True
    return False

def reset():
    mycursor.execute("UPDATE User SET total = %s, clocking = %s", (0, False))
    db.commit()

def add(userTag, time):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    total = (int) (result[1] + time)
    mycursor.execute("UPDATE User SET total = %s WHERE Tag = %s", (total, userTag))
    db.commit()

def status(userTag):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    print(result)

def list():
    mycursor.execute("SELECT * FROM User ORDER BY total DESC")
    result = mycursor.fetchall()
    print(result)
    return(result)

list()