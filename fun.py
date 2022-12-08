from telegram import *
import os
from dotenv import load_dotenv
from telegram.ext import *
import json
import requests as req

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"使用方法:\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"/img [文字]\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"/txt [文字]\n")

def test(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm no a bot, please talk to me!")

dd = {
    'url' : {
        'img' : 'https://api.openai.com/v1/images/generations',
        'text' : 'https://api.openai.com/v1/completions'
    },
    'header' : {
        'Content-Type': 'application/json',
        'Authorization': ''
    },
    'data' : {
        'img': {
            "prompt": '',
            "n": 1, 
            "size": "1024x1024"
        },
        'text': {
            'model':'babbage-search-document',
            'prompt': ''
        }
    }
}
def set_header():
    auth = os.getenv('AUTH')
    dd['header']['Authorization'] = os.getenv('OPENAI')

def img(update: Update, context: CallbackContext):
    text = update.message.text[5:]
    dd['data']['img']['prompt'] = text
    # print(dd['data'])
    res = json.loads(req.post(dd['url']['img'], headers=dd['header'], json=dd['data']['img']).text)
    for url in res['data']:
        rsp = req.get(url['url'])
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url['url'])
        print('{} printed {}'.format(update.message.chat.username, url['url']), file=sys.stderr)

def txt(update: Update, context: CallbackContext):
    text = update.message.text[5:]
    dd['data']['text']['prompt'] = text
    res = json.loads(req.post(dd['url']['text'], headers=dd['header'], json=dd['data']['text']).text)
    context.bot.send_message(chat_id=update.message.chat_id, text=res['choices'][0]['text'])
