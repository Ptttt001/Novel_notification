import sqlite3
async def add_user(UserID, domainname, title):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    c.execute('INSERT INTO user(userid,domainname,title) VALUES(?,?,?)',(UserID,domainname,title))
    conn.commit()
    #print all the data
    c.execute('SELECT * FROM user')
    print(c.fetchall())
    conn.close()

async def is_already_subscribed(UserID, domainname,  title):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE userid=? AND domainname=? AND title=?',(UserID,domainname,title))
    if c.fetchone():
        return True
    else:
        return False
    conn.close()

async def check_and_add_noval(title,ep):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM noval WHERE title=?',(title,))
    if c.fetchone():
        return 
    else:
        c.execute('INSERT INTO noval(title,ep) VALUES(?,?)',(title,ep))
        conn.commit()
    conn.close()
async def check_and_add_website(domainname,url):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM website WHERE domainname=?',(domainname,))
    if c.fetchone():
        return 
    else:
        format_phaser(url)
        c.execute('INSERT INTO website(domainname,format) VALUES(?,?)',(domainname,format_phaser(url)))
        conn.commit()
    conn.close()
async def check_and_add_have(domainname,title,indexs):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM have WHERE domainname=? AND title=? AND indexs=?',(domainname,title,indexs))
    if c.fetchone():
        return 
    else:
        c.execute('INSERT INTO have(domainname,title,indexs) VALUES(?,?,?)',(domainname,title,indexs))
        conn.commit()
    conn.close()
def update_ep(collection):
    conn = sqlite3.connect('sqlite_storage/notification.db')
    c = conn.cursor()
    for i in collection:
        title=i[0]
        recent_ep=i[1]
        c.execute('UPDATE noval SET ep=? WHERE title=?',(recent_ep,title))
        conn.commit()
    conn.close()
    return

    


async def user_subscribed(UserID, domainname, title,ep,url,index):
    await check_and_add_noval(title,ep)
    await check_and_add_website(domainname,url)
    await check_and_add_have(domainname,title,index)
    await add_user(UserID,domainname,title)

def format_phaser(url):
    #url=https://78novel.com/Book/Indexd3/bookshow/bookId/5209.html
    #set the format to https://78novel.com/Book/Indexd3/bookshow/bookId/{index}.html
    url=url.split('/')
    url[-1]='index.html'
    url='/'.join(url)
    return url

