from fastapi import FastAPI, Response, status, Request
import update_dns as dns
from main_methods import *
from classes import *
from logger import *
import datetime as dt

# update DNS
dns.main()

app = FastAPI()
methods = main_methods()
logger = systemlogger()

@app.get("/")
def read_root():
    return {"OK"}

@app.post("/send_data")
def save_data(vals: DictItem):
    try:
        conn, cursor = methods.connect_db()
        logger.LogEntry("UID: " + vals.uid)
        cursor.execute("INSERT INTO uid_data (uid, timestamp) VALUES (?, ?)", (vals.uid, dt.datetime.now().isoformat()))
        conn.commit()
        cursor.execute("INSERT INTO dict_data (uid, oid, data) VALUES (?, ?, ?)", (vals.uid, vals.oid, str(vals.data)))
        conn.commit()
        methods.close_db(conn, cursor)
        return {"OK"}
    except Exception as e:
        logger.LogEntry(str(e))
        return {"Error: " + str(e)}
    
@app.post("/get_data")
def find_data(vals: DictItemGet):
    conn, cursor = methods.connect_db()
    logger.LogEntry("UID: " + vals.uid)
    query = "SELECT data from dict_data WHERE uid = ? AND oid = ?"
    try:
        cursor.execute(query, (vals.uid, vals.oid))
        output = cursor.fetchall()
        data = []
        for row in output:
            data.append(row)
        conn.commit()
        methods.close_db(conn, cursor)
        return data
    except Exception as e:
        logger.LogEntry(str(e))
        return {"Error: " + str(e)}