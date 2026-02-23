import pymysql
host, user, password = "localhost","root","1"
connection = pymysql.connect(host=host, user=user, password=password, database="hh_db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS USERS")
query = """CREATE TABLE USERS( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME VARCHAR(255) NOT NULL, PASSWORD VARCHAR(255) NOT NULL, SCHOOL_ID INTEGER)"""
query = """CREATE TABLE USERS ( 
         user_id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
         name VARCHAR(255) NOT NULL,  
         password_hash VARCHAR(128),
         school_id INTEGER ) """
cursor.execute(query)
connection.commit()
connection.close()