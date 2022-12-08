from telegram import *
import os
from dotenv import load_dotenv
from telegram.ext import *
import json
import requests as req

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.effective_user.first_name}! I'm a not bot, please talk to me!")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"使用方法: /img [文字]\n")

def test(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def text(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text[5:])

dd = {
    'header' : {
        'Content-Type': 'application/json',
        'Authorization': ''
    },
    'data' : {
        "prompt": text,
        "n": 1, 
        "size": "1024x1024"
    },
    'url' : 'https://api.openai.com/v1/images/generations'
}
def set_header():
    auth = os.getenv('AUTH')
    dd['header']['Authorization'] = auth

def img(update: Update, context: CallbackContext):
    text = update.message.text[5:]
    dd['data']['prompt'] = text
    res = json.loads(req.post(dd['url'], headers=dd['header'], json=dd['data']).text)
    for url in res['data']:
        rsp = req.get(url['url'])
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url['url'])
        print('{} printed {}'.format(update.message.chat.username, url['url']))