import pymysql
host, user, password = "localhost","root","1"
connection = pymysql.connect(host=host, user=user, password=password)
cursor = connection.cursor()
cursor.execute("CREATE DATABASE HH_DB")
cursor.execute("SHOW DATABASES")
databaseList = cursor.fetchall()
  
for database in databaseList:
  print(database)
    
connection.close()