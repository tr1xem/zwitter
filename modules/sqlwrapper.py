import os
from dotenv import load_dotenv

load_dotenv()
db_type = os.getenv('DB_TYPE', 'mysql')
if db_type == 'mysql':
    import mysql.connector as sql
    cn = sql.connect(
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
        charset=os.getenv('DB_CHARSET'),
        collation=os.getenv('DB_COLLATION')
    )
    print("Connected to MySQL")
elif db_type == 'postgres':
    import psycopg2
    cn = psycopg2.connect(
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
        sslmode='require'  # Require SSL connection
    )
    print("Connected to PostgreSQL")
else:
    raise ValueError("Unsupported DB type")

cursor = cn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20) NOT NULL PRIMARY KEY,
    password VARCHAR(20) DEFAULT NULL,
    displayname VARCHAR(20) DEFAULT NULL,
    option VARCHAR(10) DEFAULT NULL
);
"""
cursor.execute(create_table_query)
cn.commit()

def registeruser(username, password, displayname, option):
    cursor.execute("INSERT INTO users (username, password, displayname, option) VALUES (%s, %s, %s, %s)",
                   (username, password, displayname, option))
    cn.commit()

def loginuser(username, password):
    print(username, password)
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return False

def getuser(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchall()
    return result[0]

def checkuser(username):
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    result = cursor.fetchall()
    if result[0][0] == 0:
        return True
    else:
        return False
