from fastapi import FastAPI, Response, status, Request
from main_methods import *
from classes import *
from logger import *
import datetime as dt

app = FastAPI()
methods = main_methods()
logger = systemlogger()

@app.get("/")
def read_root():
    return {"OK"}

@app.post("/dict-save")
async def dict_save(vals: DictItem):
    try:
        conn, cursor = methods.connect_db()
        logger.LogEntry("UID: " + vals.uid)
        cursor.execute("INSERT INTO uid_data (uid, timestamp) VALUES (?, ?)", (vals.uid, dt.datetime.now().isoformat()))
        conn.commit()
        cursor.execute("INSERT INTO dict_data (uid, data) VALUES (?, ?)", (vals.uid, str(vals.data)))
        conn.commit()
        methods.close_db(conn, cursor)
        return {"OK"}
    except Exception as e:
        logger.LogEntry(str(e))
        return {"Error: " + str(e)}
    

