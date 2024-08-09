from flask import Flask, request, abort
import os
import sqlite3
import requests
from bs4 import BeautifulSoup
import asyncio

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration,ApiClient,MessagingApi,ReplyMessageRequest,TextMessage
from linebot.v3.webhooks import MessageEvent,TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

import databaseLib

app = Flask(__name__)


configuration = Configuration(access_token='q8jsC+r72gu80rKQ3zx589kAJf1vjR7i0T9K8OANFWEl2fS4XbjbDRoOT+GfCuGWJM5tUhfBTjCOkqgvNA4Z2EDIEAf/R28n+VpTGL3EcVP1Np7uslE2WyH4pFrw41NsBtKh4zezMaQLdkO+WO5U2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8485989bb170b428a3e6bab0aa413f01')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        #get the user id, title and index
        user_id = event.source.user_id
        title=get_title(event.message.text)
        index=get_index(event.message.text)
        domain=event.message.text.split('/')[2]
        print("Somebody subscribe"+title[0],index,domain,user_id)

        #check if the user has already subscribed
        if asyncio.run(databaseLib.is_already_subscribed(user_id,index,domain)):
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="您已經訂閱過了: "+title[0])]))
            return
        
        #write the subscription into the database
        asyncio.run(databaseLib.add_user(user_id,index,domain))
        #return the subscription content
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="已為您訂閱: "+title[0])]
            )
        )
        
def get_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_divs = soup.find_all('div', class_='details_top_left_top')
    title = [div.find('h3').get_text() for div in title_divs if div.find('h3')]
    return title
def get_index(url):
    index=url.split('/')[-1].split('.')[0]
    return index
def add_subscription(userID,website,Subscription):
    
    return



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)