import os
from dotenv import load_dotenv

load_dotenv()
# cn =  sql.connect(user='root', password='root', host='localhost',database='login',    charset='utf8mb4', collation='utf8mb4_general_ci')
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
elif db_type == 'postgres':
    import psycopg2
    cn = psycopg2.connect(
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
                sslmode='require'  # Require SSL connection

    )
else:
    raise ValueError("Unsupported DB type")
cursor  =  cn.cursor()
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

def registeruser(username,password,displayname,option):
    cursor.execute(f"INSERT INTO users (username,password,displayname,option) VALUES ('{username}','{password}','{displayname}','{option}')")
    cn.commit()


def  loginuser(username,password):
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = '{username}' AND password = '{password}'")
    result = cursor.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return  False

def getuser(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    result = cursor.fetchall()
    return result[0]


def checkuser(username):
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = '{username}'")
    result = cursor.fetchall()
    if result[0][0] == 0:
        return True
    else:
        return  False
