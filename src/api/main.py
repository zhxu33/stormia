from fastapi import FastAPI
from data import db, mycursor

app = FastAPI()

from datetime import datetime

def convert_time(current_dateTime):
    return "`"+str(current_dateTime.month)+"/"+str(current_dateTime.day)+"/"+str(current_dateTime.year)+" | "+str(current_dateTime.hour)+":"+str(current_dateTime.minute)+":"+str(current_dateTime.second) + " PST`."

def convert_seconds(seconds):
    return "`"+str(round(seconds/3600, 2))+"`"

def convert_minutes(time):
    return "`"+str(round(time/60, 2))+"`"

def ping(id): 
    return "<@" + str(id) + '>'

@app.get("/")
async def commandList():
    commands = ["!dl commands", "!dl insert @user", "!dl drop @user", "!dl status @user", "!dl status", "!dl add time", "!dl add time @user", "!dl list", "!dl clockin", "!dl clockout", "!dl reset", "!dl reset @user"]
    return {"message": '`' + '\n'.join(commands) + '`'}

@app.put("/resume/{id}")
async def resume(id):
    try:
        current_dateTime = datetime.now()
        mycursor.execute("SELECT * FROM User WHERE tag = %s", [id])
        result = mycursor.fetchone()
        if (str(result)=="None"):
            return "User not found in database."
        if result[3] == False:
            mycursor.execute("UPDATE User SET clocking = %s, start = %s WHERE Tag = %s", (True, current_dateTime, id))
            db.commit()
            return {"message": "You have clocked in at "+convert_time(current_dateTime)}
        else:
            return {"message": "User is already in session."}
    except:
        return {"message": "Failed to access user data."}

@app.put("/pause/{id}")
async def pause(id):
    try:
        current_dateTime = datetime.now()
        mycursor.execute("SELECT * FROM User WHERE tag = %s", [id])
        result = mycursor.fetchone()
        if (str(result)=="None"):
            return {"message": "User not found in database."}
        if result[3] == True:
            total = (int) (result[1] + (current_dateTime-result[2]).total_seconds())
            mycursor.execute("UPDATE User SET total = %s, clocking = %s WHERE Tag = %s AND clocking = %s", (total, False, id, True))
            db.commit()
            return {"message": "You have clocked out at "+convert_time(current_dateTime)+"\nSession Hours: "+convert_seconds(total)+"(+"+convert_seconds((current_dateTime-result[2]).total_seconds())+")"}
        else:
            return {"message": "User is not in session."}
    except:
        return {"message": "Failed to access user data."}

@app.post("/insert/{id}")
async def insert(id):
    try:
        mycursor.execute("INSERT INTO User (tag, total, start, clocking) VALUES (%s,%s,%s,%s)", (id, 0, datetime.now(), False))
        db.commit()
        return {"message": f"Successfully added {ping(id)} to the database."}
    except:
        return {"message": f"{ping(id)} is already on the database."}

@app.delete("/drop/{id}")
async def drop(id):
    try:
        mycursor.execute("DELETE FROM User WHERE tag = %s", [id])
        db.commit()
        return {"message": f"Successfully removed {ping(id)} from the database."}
    except:
        return {"message": f"{ping(id)} is not on the database."}

@app.put("/reset/{id}")
async def resetUser(id):
    try:
        prev = await status(id)
        mycursor.execute("UPDATE User SET total = %s, clocking = %s WHERE tag = %s", (0, False, id))
        db.commit()
        after = await status(id)
        return {"message": prev["message"]+"\n=>\nSuccessfully reset user data.\n"+after["message"]}
    except:
        return {"message": "Failed to reset user data."}

@app.put("/reset")
async def reset():
    try:
        prev = await list()
        mycursor.execute("UPDATE User SET total = %s, clocking = %s", (0, False))
        db.commit()
        after = await list()
        return {"message": prev["message"]+"=>\nSuccessfully reset database.\n"+after["message"]}
    except:
        return {"message": "Failed to reset database."}

@app.put("/add/{time}/{id}")
async def add(time: int, id):
    try:
        mycursor.execute("SELECT * FROM User WHERE tag = %s", [id])
        result = mycursor.fetchone()
        total = (int) (result[1] + time*60)
        mycursor.execute("UPDATE User SET total = %s WHERE Tag = %s", (total, id))
        db.commit()
        return {"message": f"{ping(id)}"+" Session Hours: "+convert_seconds(total)+"(+"+convert_minutes(time)+")"}
    except:
        return {"message": "User not found."}

@app.get("/status/{id}")
async def status(id):
    try:
        mycursor.execute("SELECT * FROM User WHERE tag = %s", [id])
        result = mycursor.fetchone()
        return {"message": f"{ping(id)} Session Hours: `{convert_seconds(result[1])}`"}
    except:
        return {"message": "User not found."}

@app.get("/list")
async def list():
    try:
        mycursor.execute("SELECT * FROM User ORDER BY total DESC")
        result = mycursor.fetchall()
        s = ""
        for x in result:
            id, time = x[0:2]
            s = s+f"{ping(id)} Session Hours: `{convert_seconds(time)}`\n"
        return {"message": s}
    except:
        return {"message": "Data not found."}

import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('apihost')
port = os.getenv('port')

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=int(port)) # 233050942742855680