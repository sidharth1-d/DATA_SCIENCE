import mysql.connector

db_server = mysql.connector.connect(
    host = "local",
    user = "root",
    password = "root",

)

cursor = db_server.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS cric_db_mysql")
cursor.execute("USE cric_db_mysql")

cursor.execute('''
               CREATE TABLE IF NOT EXISTS
               players(
               jerNo INT PRIMARY KEY,
               playerName VARCHAR(100)
               avg DOUBLE
               )
               ''')

sql ="INSERT INTO players (jerNo,playerName,avg ) VALUES (%s ,%s, %s) ON DUPLICATE KEY UPDATE playerName = Value (playerName)"
val = (45,"rohit sharma",48.2)

cursor.execute(sql,val)
db_server.commit()

print("step 2 complete : connected to mysql server and created 'cric_db_mysql'.")
db_server.close()