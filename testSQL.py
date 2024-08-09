#show data in sqlite
import sqlite3
con = sqlite3.connect('notification.db')
cursorObj = con.cursor()
cursorObj.execute('SELECT * FROM usersubscription')
rows = cursorObj.fetchall()
for row in rows:
    print(row)
con.close()
