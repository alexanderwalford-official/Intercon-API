from fastapi import FastAPI, Response, status, Request
from fastapi.templating import Jinja2Templates
import update_dns as dns
import create_tables as tb_cr
from main_methods import *
from classes import *
from logger import *
import datetime as dt

API_STATUS = "ONLINE"

# update DNS
dns.main()

# ensure tables exist
tb_cr.main()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
methods = main_methods()
logger = systemlogger()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
def read_status():
    # check connection to DB
    DB_OK = False
    try:
        conn, cursor = methods.connect_db()
        DB_OK = True
    except Exception as e:
        DB_OK = False
    return_dict = {"db_connection": str(DB_OK), "api_status": API_STATUS}
    return return_dict

@app.post("/send_data")
def save_data(vals: DictItem):
    if methods.check_api_key(vals.api_key):
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
    else:
        return {"Error: Invalid API key!"}

    
@app.post("/get_data")
def find_data(vals: DictItemGet):
    if methods.check_api_key(vals.api_key):
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
    else:
        return {"Error: Invalid API key!"}
    
@app.post("/get_custom_query")
def get_custom_query(vals: DataItemTable):
    """
        Allows the user to send their own SQL query and get the returned data.
    """
    blocked_tables = ["users", "api_keys"]
    if methods.check_api_key(vals.api_key):
        if vals.table not in blocked_tables:
            conn, cursor = methods.connect_db()
            logger.LogEntry("UID: " + vals.uid)
            query = vals.action + " " + vals.identifier + " FROM " + vals.table + " WHERE " + vals.identifier + " = " + vals.match
            cursor.execute(query)
            output = cursor.fetchall()
            data = []
            for row in output:
                data.append(row)
            conn.commit()
            methods.close_db(conn, cursor)
            return data
        else:
            return {"Error: You tried to access a restricted table!"}
    else:
        return {"Error: Invalid API key!"}


@app.post("/save_custom_query")
def save_custom_query(vals: DataItemTableSave):
    """
        Allows the user to send their own SQL query to save data.
    """
    blocked_tables = ["users", "api_keys"]
    if methods.check_api_key(vals.api_key):
        if vals.table not in blocked_tables:
            conn, cursor = methods.connect_db()
            logger.LogEntry("UID: " + vals.uid)
            query = "INSERT INTO " + vals.table + "( " + vals.cols + ",) VALUES (" + vals.vals + ",)"
            cursor.execute(query)
            output = cursor.fetchall()
            return output
        else:
            return {"Error: You tried to access a restricted table!"}
    else:
        return {"Error: Invalid API key!"}
