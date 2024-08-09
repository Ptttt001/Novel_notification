import sqlite3
async def add_user(UserID, Subscription, Website):
    conn = sqlite3.connect('notification.db')
    c = conn.cursor()
    c.execute('INSERT INTO usersubscription(userID,website,Subscription) VALUES(?,?,?)',(UserID,Website,Subscription))
    conn.commit()
    #print all the data
    c.execute('SELECT * FROM usersubscription')
    print(c.fetchall())
    conn.close()

async def is_already_subscribed(UserID, Subscription, Website):
    conn = sqlite3.connect('notification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usersubscription WHERE userID=? AND website=? AND Subscription=?',(UserID,Website,Subscription))
    if c.fetchone():
        return True
    else:
        return False
    conn.close()