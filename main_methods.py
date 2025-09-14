import sqlite3
import uuid

class main_methods:
    def __init__(self):
        pass

    def generate_uid(self):
        import uuid
        return str(uuid.uuid4())

    def connect_db(self):
        conn = sqlite3.connect('mainframe.db')
        cursor = conn.cursor()
        return conn, cursor

    def close_db(self, conn, cursor):
        cursor.close()
        conn.close()

    def check_api_key(self, key):
        conn, cursor = self.connect_db()
        query = "SELECT key from api_keys WHERE key = ?"
        try:
            cursor.execute(query, (key,))
            output = cursor.fetchone()
            self.close_db(conn, cursor)
            if output:
                return True
            else:
                return False
        except:
            return False
        
    def get_admin_email_from_auth (self, request):
        key = request.cookies.get("auth_key")
        conn, cursor = self.connect_db()
        query = "SELECT email FROM auth_tokens WHERE uid = ?"
        cursor.execute(query, (key,))
        email = str(cursor.fetchall()[0][0])
        conn.commit()
        self.close_db(conn, cursor)
        return email
    
    def get_priv_from_email(self, email):
        conn, cursor = self.connect_db()
        query = "SELECT perms FROM users WHERE email = ?"
        cursor.execute(query, (email,))
        output = cursor.fetchall()[0][0]
        conn.commit()
        self.close_db(conn, cursor)
        return output
    
    def get_api_key_from_email (self, email):
        # get user API key
        conn, cursor = self.connect_db()
        query = "SELECT * FROM api_keys WHERE email = ?"
        cursor.execute(query, (email,))
        account_keys = cursor.fetchall()
        conn.commit()
        self.close_db(conn, cursor)
        return account_keys
    
    def generate_api_keys_account(self, email):
        api_key = str(uuid.uuid4())
        conn, cursor = self.connect_db()
        query = "INSERT INTO api_keys (email, key, perms) VALUES (?, ?, ?)"
        cursor.execute(query, (email, api_key, 5))
        conn.commit()
        self.close_db(conn, cursor)
        return True
    
    def execute_query (self, query):
        conn, cursor = self.connect_db()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        return data