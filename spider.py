#get all the noval and their own noval from the database
import sqlite3
import requests
from bs4 import BeautifulSoup

import key
import databaseLib
import asyncio
import time

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration,ApiClient,MessagingApi,PushMessageRequest,TextMessage

async def send_message(UserID, title,recent_ep,url,ep_num):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message_with_http_info(
            PushMessageRequest(
                to=UserID,
                messages=[TextMessage(text="您的訂閱["+title+"]有"+ep_num+"個更新，已至"+str(recent_ep)+"集"+url)]
            )
        )
    return


print("start spider")
con = sqlite3.connect('notification.db')
cursorObj = con.cursor()
cursorObj.execute('''SELECT
    noval.title,
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
#traverse the result and spider the noval
notify_list=[]

for row in cursorObj.fetchall():
    #the result =[(1294, 'https://78novel.com/Book/Indexd3/bookshow/bookId/index.html', '5209')]
    #get the ep, format, index
    time.sleep(0.5)
    title=row[0]
    ep=(row[1])
    format=row[2]
    index=row[3]
    #combine the url
    url=format.replace('index',index)
    #get the response
    response = requests.get(url)
    #parse the response
    soup = BeautifulSoup(response.text, 'html.parser')
    #get the content
    recent_ep=int(soup.find('span', class_='pull-right').get_text()[2:-3])
    #compare the ep
    print(ep,recent_ep)
    if ep!=recent_ep:
        #send the message to the user
        new_collect=[title,recent_ep,url,str(recent_ep-ep)]
        notify_list.append(new_collect)
        print("send the message to the user")
        #add the book to a list

if len(notify_list)==0:
    exit()
#send the message to users
configuration = Configuration(access_token=key.my_access_token)
handler = WebhookHandler(key.my_WebhookHandler)
for i in notify_list:
    #search the user who subscribed the book
    cursorObj.execute('SELECT userid FROM user WHERE title=?',(i[0],))
    #get the user id
    user_id=cursorObj.fetchall()
    for j in user_id:
        #send the message to the user
        asyncio.run(send_message(j[0],i[0],i[1],i[2],i[3]))

databaseLib.update_ep(notify_list)
con.close()

