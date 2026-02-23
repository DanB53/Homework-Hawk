import pymysql
import secrets
from werkzeug.security import generate_password_hash

hashedPassword = generate_password_hash("1")
print(hashedPassword)


host, user, password = "localhost","root","1"
connection = pymysql.connect(host=host, user=user, password=password, database="hh_db")
cursor = connection.cursor()
id = 1
cursor.execute(f"SELECT user_id FROM USERS WHERE user_id = {id}")
row = cursor.fetchone()
print(row)
if row is not None:
    print("Another userid with the same text exists.")
else:
    print("No other userid with the same text exists.")
    name = "a"
    password = "1"
    hashedPassword = generate_password_hash(password)
    print(hashedPassword)
    school_id = 1
    cursor.execute(f"INSERT INTO USERS (name,password_hash,school_id,admin_account) VALUES ('{name}', '{hashedPassword}',1,false)")
    connection.commit()
    print("Success")


id = 2
cursor.execute(f"SELECT user_id FROM USERS WHERE user_id = {id}")
row = cursor.fetchone()
print(row)
if row is not None:
    print("Another userid with the same text exists.")
else:
    print("No other userid with the same text exists.")
    name = "b"
    password = "1"
    hashedPassword = generate_password_hash(password)
    print(hashedPassword)
    school_id = 2
    cursor.execute(f"INSERT INTO USERS (name,password_hash,school_id,admin_account) VALUES ('{name}', '{hashedPassword}',1,true)")
    connection.commit()
    print("Success")



school_name = "Wab School"

cursor.execute(f"SELECT name FROM schools WHERE name = 'Wab School'")
row = cursor.fetchone()
print(row)
if row is not None:
    print("Another school name with the same text exists.")
else:
    print("No other school name with the same text exists.")

    cursor.execute(f"INSERT INTO schools (name,admin_user_id) VALUES ('{school_name}', '{1}')")
    connection.commit()
    print("Success")