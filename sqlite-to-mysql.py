import sqlite3
import mysql.connector

sqlite_conn = sqlite3.connect("cric_player.db")
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute("SELECT * FROM players")
all_players = sqlite_cursor.fetchall()

sqlite_conn.close()

mysql_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "cric_db_mysql"
)

mysql_cursor = mysql_db.cursor()

mysql_query = "INSERT IGNORE INTO players(jerNo,playerName,avg) VALUES (%s,%s,%s)"

mysql_cursor.executemany(mysql_query,all_players)
mysql_db.commit()

print(f"step 3 complete : migrated{mysql_cursor.rowcount} players from SQLite to MySQL !")

mysql_db.close()