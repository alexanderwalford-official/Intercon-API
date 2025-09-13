import sqlite3

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