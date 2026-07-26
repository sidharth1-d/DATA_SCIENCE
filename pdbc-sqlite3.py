import sqlite3
conn = sqlite3.connect("cric_player.db")
cursor =  conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS
               players(
                        jerNo INTEGER PRIMARY KEY,
              playerName TEXT,
               avg REAL 
               )
               ''')
cursor.execute("INSERT OR REPLACE INTO players VALUES(18,'virat kohli',50.5)")
conn.commit()
conn.close()

print("step 1 complete : SQLite database 'cric_player.db' created with 1 player.")
