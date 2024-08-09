import sqlite3
con = sqlite3.connect('notification.db')
cursorObj = con.cursor()
cursorObj.execute('CREATE TABLE usersubscription (userID text, website text,Subscription text)')
#set the primary key
cursorObj.execute('CREATE UNIQUE INDEX idx_usersubscription ON usersubscription (userID,website)')
con.commit()
#insert data
cursorObj.execute('INSERT INTO usersubscription(userID,website,Subscription) VALUES(1234,1,1211)')
con.commit()