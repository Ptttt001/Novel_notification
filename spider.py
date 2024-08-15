#get all the noval and their own noval from the database
import sqlite3
import requests
from bs4 import BeautifulSoup
con = sqlite3.connect('notification.db')
cursorObj = con.cursor()
cursorObj.execute('''SELECT 
    noval.ep, 
    website.format, 
    have.indexs
FROM 
    noval
JOIN 
    have ON noval.title = have.title
JOIN 
    website ON have.domainname = website.domainname;
''')
print(cursorObj.fetchall())
#traverse the result and spider the noval
for row in cursorObj.fetchall():
    #the result =[(1294, 'https://78novel.com/Book/Indexd3/bookshow/bookId/index.html', '5209')]
    #get the ep, format, index
    ep=row[0]
    format=row[1]
    index=row[2]
    #combine the url
    url=format.replace('index',index)
    #get the response
    response = requests.get(url)
    #parse the response
    soup = BeautifulSoup(response.text, 'html.parser')
    #get the content
    ep=soup.find('span', class_='pull-right').get_text()
    #compare the ep
    if ep!=ep:
        #send the message to the user
        print("send the message to the user")
        #update the ep
        #cursorObj.execute('UPDATE noval SET ep=? WHERE title=?',(ep,row[3]))
        #con.commit()
