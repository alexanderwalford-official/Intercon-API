import sqlite3

# path to your SQL file
sql_file_path = "structure.sql" 

# connect to the SQLite database
connection_obj = sqlite3.connect("mainframe.db")

# create a cursor object to interact with the database
cursor_obj = connection_obj.cursor()

# read the SQL file
with open(sql_file_path, "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()

# execute the SQL script
cursor_obj.executescript(sql_script)

# commit changes
connection_obj.commit()

print("Database schema has been created from SQL file.")

# close the connection to the database
connection_obj.close()
