# import import_lib
import os
import sys
import json
import logging
import requests as req
from time import sleep
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv
# from pytube.cli import on_progress
from pytube import YouTube as Youtube
import openai


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = \
    """
    使用方法:
    圖片生成: /img [文字]
    IG貼文圖片抓取: /ig [IG網址]
    YT MP3下載: /yt [YT網址]
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def get_img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(text=f"生成中...", reply_markup=None)
    imgNums, text = query.data.split(' ', 1)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv('OPENAI_TOKEN'),
    }
    body = {
        'prompt': text,
        'n': int(imgNums),
        'size': '1024x1024'
    }

    res = json.loads(req.post('https://api.openai.com/v1/images/generations', headers=headers, json=body).text)
    for url in res['data']:
        await context.bot.send_photo(update.callback_query.message.chat.id, photo=url['url'])

    await context.bot.send_message(chat_id=update.callback_query.message.chat.id, text='生成完畢 uwu',reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("重新生成", callback_data=query.data)]]))

async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text[4:]
    test = 'cute animate girl' if text == '' else text

    MAXN = 5
    await update.message.reply_text('選擇要生成幾張圖片', reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(str(x), callback_data=f'{x}'+text) for x in range(1, MAXN+1)
    ]]))
    return get_img

async def yt(update: Update, context: CallbackContext):
    url = update.message.text[4:]
    if url == '':
        await context.bot.send_message(chat_id=update.message.chat_id, text='請貼上連結 >w<')
        return
    msg = await context.bot.send_message(chat_id=update.message.chat_id, text='下載中...')
    yt = Youtube(url)
    # yt = Youtube(url,on_progress_callback=on_progress)
    file = yt.streams.filter().get_audio_only().title + '.mp3'
    yt.streams.filter(only_audio=True).first().download(filename=file)
    msg = await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text='下載完畢')
    msg = await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text='上傳中...')
    await context.bot.send_audio(chat_id=update.message.chat.id, audio=open(file, 'rb'), write_timeout=1000, read_timeout=1000)
    msg = await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text='上傳完畢')
    print(file)
    os.remove(file)