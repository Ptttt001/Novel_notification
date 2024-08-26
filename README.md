# Noval Notification

## Description
This is a project that can let user subscribe to a noval and get notification when the noval has new chapter.
The noval is base on the website [https://78novel.com/homepage](https://78novel.com/homepage). 
The user can subscribe to the noval by sending the url to Linebot. 
When the noval has a new chapter, the Linebot will send a message to the user to notify the user.
## Features
- User can get notification when they join our lone account and subscribe to a noval.
- User can get notification when the noval has new chapter.
## some example
- Send url 
- get notification
## requirement
- Python 
- Flask
- line-bot-sdk
- beautifulsoup4
## Usage
This project have two part, one is the server side and the other is the crawler side.
The server side is a flask server used to receive the request from Linebot. 
The crawler side is a crawler used to get the information of the noval and every 10 minutes.
- local
```bash
# Linux like
gunicorn -b 0.0.0.0:80 app:app 
# Windows
python app.py
```
- docker
```bash
# flask
docker build -t notification -f .\dockerfile_flask .
# crawler
docker build -t crawler -f .\dockerfile_spider .
```
## sqlite image
```bash
#run
docker run -p 6336:6336 -v ${PWD}/sqlite_storage:/sqlite/storage:z keinos/sqlite3
```
