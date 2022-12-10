from telegram import *
import os
from dotenv import load_dotenv
from telegram.ext import *
import json
import requests as req

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"使用方法:\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"/p [文字]\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"/t [文字]\n")

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

def get_img(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    dd['data']['img']['n'] = int(query.data[:1])
    dd['data']['img']['prompt'] = query.data[1:]
    res = json.loads(req.post(dd['url']['img'], headers=dd['header'], json=dd['data']['img']).text)
    query.edit_message_text(text=f"生成中...")
    for url in res['data']:
        rsp = req.get(url['url'])
        context.bot.send_photo(update.callback_query.message.chat.id, photo=url['url'])
    context.bot.send_message(chat_id=update.callback_query.message.chat.id, text='生成完畢 uwu',reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("重新生成", callback_data=query.data)]]))

def img(update: Update, context: CallbackContext):
    text = update.message.text
    if update.message.text[:4] == '/img':
        text = update.message.text[5:]
    else:
        text = update.message.text[3:]
    if text == '':
        text = 'cute animate girl'

    MAXN = 5
    update.message.reply_text('選擇要生成幾張圖片', reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(str(x), callback_data=f'{x}'+text) for x in range(1, MAXN+1)
    ]]))
    return get_img

def txt(update: Update, context: CallbackContext):
    text = update.message.text
    if update.message.text[:4] == '/txt':
        text = update.message.text[5:]
    else:
        text = update.message.text[3:]
    if text == '':
        text = 'cute animate cat girl'
    dd['data']['text']['prompt'] = text
    res = json.loads(req.post(dd['url']['text'], headers=dd['header'], json=dd['data']['text']).text)
    context.bot.send_message(chat_id=update.message.chat_id, text=res['choices'][0]['text'])
