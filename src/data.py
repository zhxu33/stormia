import mysql.connector
from datetime import datetime
from info import *
import time

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = passwd,
    database = database
    )

mycursor = db.cursor()
#mycursor.execute("CREATE TABLE User (tag VARCHAR(50) PRIMARY KEY, total int, start datetime, clocking bool)")
# mycursor.execute("DROP TABLE User")

def convert_time(current_dateTime):
    return "`"+str(current_dateTime.month)+"/"+str(current_dateTime.day)+"/"+str(current_dateTime.year)+" | "+str(current_dateTime.hour)+":"+str(current_dateTime.minute)+":"+str(current_dateTime.second) + " PST`."

def convert_seconds(seconds):
    return "`"+str(round(seconds/3600, 2))+"`"

def convert_minutes(time):
    return "`"+str(round(time/60, 2))+"`"

def resume(userTag):
    current_dateTime = datetime.now()
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if (str(result)=="None"):
        return "User not found in database."
    if result[3] == False:
        mycursor.execute("UPDATE User SET clocking = %s, start = %s WHERE Tag = %s", (True, current_dateTime, userTag))
        db.commit()
        return "You have resumed at "+convert_time(current_dateTime)
    else:
        return "User is already in session."

def pause(userTag):
    current_dateTime = datetime.now()
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if (str(result)=="None"):
        return "User not found in database."
    if result[3] == True:
        total = (int) (result[1] + (current_dateTime-result[2]).total_seconds())
        mycursor.execute("UPDATE User SET total = %s, clocking = %s WHERE Tag = %s AND clocking = %s", (total, False, userTag, True))
        db.commit()
        return "You have paused at "+convert_time(current_dateTime)+"\nSession Hours: "+convert_seconds(total)+"(+"+convert_seconds((current_dateTime-result[2]).total_seconds())+")"
    else:
        return "User is not in session."

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
    prev = list()
    mycursor.execute("UPDATE User SET total = %s, clocking = %s", (0, False))
    db.commit()
    return prev+"=>\nSuccessfully reset database.\n"+list()

def add(userTag, time):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if (str(result) != "None"):
        total = (int) (result[1] + time*60)
        mycursor.execute("UPDATE User SET total = %s WHERE Tag = %s", (total, userTag))
        db.commit()
        return f"{userTag}"+" Session Hours: "+convert_seconds(total)+"(+"+convert_minutes(time)+")"
    else:
        return "User not found in database."

def status(userTag):
    mycursor.execute("SELECT * FROM User WHERE tag = %s", [userTag])
    result = mycursor.fetchone()
    if (str(result) != "None"):
        return f"{result[0]} Session Hours: `{convert_seconds(result[1])}`"
    else:
        return "User not found in database."

def list():
    mycursor.execute("SELECT * FROM User ORDER BY total DESC")
    result = mycursor.fetchall()
    if (str(result) != "None"):
        s = ""
        for x in result:
            x = x[0:2]
            s = s+f"{x[0]} Session Hours: `{convert_seconds(x[1])}`\n"
        return s
    else:
        return "Data not found."