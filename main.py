from fastapi import FastAPI, Response, status, Request, HTTPException
from fastapi.templating import Jinja2Templates
import update_dns as dns
import create_tables as tb_cr
from main_methods import *
from classes import *
from logger import *
import datetime as dt
from passlib.context import CryptContext
import uuid
from fastapi.middleware.cors import CORSMiddleware

API_STATUS = "ONLINE"

# Configure hashing context (bcrypt is a solid default)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# update DNS
dns.main()

# ensure tables exist
tb_cr.main()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
methods = main_methods()
logger = systemlogger()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/privacy")
def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.get("/admin")
def admin(request: Request):
    email = methods.get_admin_email_from_auth(request)
    priv = methods.get_priv_from_email(email)
    if priv > 0:
        users = methods.execute_query("SELECT * FROM users")
        account_keys = methods.get_api_key_from_email(email)
        if not account_keys:
            methods.generate_api_keys_account(email)
        return templates.TemplateResponse("sql_admin.html", {"request": request, "users": users, "account_keys": account_keys})
    else:
        return {"Error! You either do not have permission to access this page."}

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
    blocked_tables = ["users", "api_keys", "product_versions"]
    if methods.check_api_key(vals.api_key):
        if vals.table not in blocked_tables:
            conn, cursor = methods.connect_db()
            query = "INSERT INTO " + vals.table + "( " + vals.cols + ", uid, oid) VALUES ('" + vals.vals + "', '" + vals.uid + "', '" + vals.cols + "')"
            cursor.execute(query)
            methods.close_db(conn, cursor)
            return {"OK"}
        else:
            return {"Error: You tried to access a restricted table!"}
    else:
        return {"Error: Invalid API key!"}

@app.post("/register-user")
def register_user(vals: UserLogin):
    if vals.email.strip() == "" or vals.password.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blank email or password"
        )

    logger.LogEntry("Registering new user.")
    conn, cursor = methods.connect_db()

    # check if user already exists
    query = "SELECT id FROM users WHERE email = ?"
    cursor.execute(query, (vals.email,))
    existing_user = cursor.fetchone()

    if existing_user:
        methods.close_db(conn, cursor)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # insert new user
    secure_password = hash_password(vals.password)
    query = "INSERT INTO users (email, password, perms) VALUES (?, ?, ?)"
    cursor.execute(query, (vals.email, secure_password, 0))
    conn.commit()

    methods.close_db(conn, cursor)
    return {"status": "success"}


@app.post("/login-user")
def login_user(response: Response, vals: UserLogin):
    conn, cursor = methods.connect_db()
    query = "SELECT password FROM users WHERE email = ?"
    cursor.execute(query, (vals.email,))
    row = cursor.fetchone()
    conn.commit()
    methods.close_db(conn, cursor)
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    stored_hash = row[0]
    
    if verify_password(vals.password, stored_hash):
        uid = str(uuid.uuid4())
        # save uid into DB
        conn, cursor = methods.connect_db()
        query = "INSERT INTO auth_tokens (uid, email) VALUES (?, ?)"
        cursor.execute(query, (uid, vals.email))
        conn.commit()
        methods.close_db(conn, cursor)
        # return cookie key
        response.set_cookie(key="auth_key", value=uid)
        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

@app.post("/admin-query")
def admin_query(response: Response, request: Request, vals:QueryItem):
    # check user priv
    email = methods.get_admin_email_from_auth(request)
    priv = methods.get_priv_from_email(email)
    if priv > 0:
        query = vals.query
        data = methods.execute_query(query)
        return data
    else:
        return {"Invalid permission!"}
    
@app.post("/save_game_data")
def game_save_data(vals:SaveDataItem):
    if methods.check_api_key(vals.api_key):
        conn, cursor = methods.connect_db()
        query = "INSERT INTO game_save_files (uid, file_name, file_content, folder, notes) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (vals.uid, vals.file_name, vals.file_content, vals.folder, vals.notes))
        conn.commit()
        methods.close_db(conn, cursor)
        return {"OK"}
    else:
        return {"Error: Invalid API key!"}
    
@app.post("/get_game_data")
def get_save_data(vals: SaveDataItemGet):
    if methods.check_api_key(vals.api_key):
        query = "SELECT * FROM game_save_files WHERE uid = ?"
        conn, cursor = methods.connect_db()
        cursor.execute(query, (vals.uid,))
        output = cursor.fetchall()
        conn.commit()
        methods.close_db(conn, cursor)
        data = []
        for row in output:
            data.append(row)
        return data
    else:
        return {"Error: Invalid API key!"}
    
@app.get("/get_product_information/{product_id}")
def get_product_version(product_id):
    # search DB to get latest version
    query = "SELECT version, url, hash FROM product_versions WHERE product = ?"
    conn, cursor = methods.connect_db()
    cursor.execute(query, (product_id,))
    output = cursor.fetchone()
    conn.commit()
    methods.close_db(conn, cursor)
    return output