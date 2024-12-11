import mysql.connector as  sql
cn =  sql.connect(user='root', password='root', host='localhost',database='login',    charset='utf8mb4',
    collation='utf8mb4_general_ci')
cursor  =  cn.cursor()
cursor.execute('select * from users')
def  showusers():
    print (cursor.fetchall())

showusers()
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
