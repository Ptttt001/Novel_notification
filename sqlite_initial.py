import sqlite3
con = sqlite3.connect('sqlite_storage/notification.db')
#noval
cursorObj = con.cursor()
cursorObj.execute('''CREATE TABLE noval (
    ep INT,
    title VARCHAR(40),
    PRIMARY KEY (title)
);
''')
con.commit()

#website
cursorObj = con.cursor()
cursorObj.execute('''CREATE TABLE website (
    domainname VARCHAR(20),
    format VARCHAR(100),
    PRIMARY KEY (domainname)
);
''')
con.commit()

#user
cursorObj = con.cursor()
cursorObj.execute('''CREATE TABLE user (
    userid VARCHAR(50),
    domainname VARCHAR(20),
    title VARCHAR(40),
    PRIMARY KEY (userid, domainname, title)
    FOREIGN KEY (domainname) REFERENCES website(domainname)
    FOREIGN KEY (title) REFERENCES noval(title)
);
''')
con.commit()

#have
cursorObj = con.cursor()
cursorObj.execute('''CREATE TABLE have (
    domainname VARCHAR(20),
    title VARCHAR(40),
    indexs VARCHAR(20),
    PRIMARY KEY (domainname, title),
    FOREIGN KEY (domainname) REFERENCES website(domainname),
    FOREIGN KEY (title) REFERENCES noval(title)
);
''')
con.commit()

#show all the table in the database
cursorObj = con.cursor()
cursorObj.execute('SELECT name from sqlite_master where type= "table"')
print(cursorObj.fetchall())