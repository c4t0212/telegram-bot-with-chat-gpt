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

async def test(update: Update, context: CallbackContext):
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
    dd['data']['img']['n'] = int(query.data[:1])
    dd['data']['img']['prompt'] = query.data[1:]
    res = json.loads(req.post(dd['url']['img'], headers=dd['header'], json=dd['data']['img']).text)
    query.edit_message_text(text=f"生成中...")
    for url in res['data']:
        rsp = req.get(url['url'])
        context.bot.send_photo(update.callback_query.message.chat.id, photo=url['url'])
    query.answer()
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

def check_element_is_exist(wb, xpath):
    try:
        wb.find_element(By.XPATH, xpath)
        return True
    except:
        return False

def get_xpath_attribute(wb : webdriver, xpath : str, attribute : str):
    return wb.find_element(By.XPATH, xpath).get_attribute(attribute)


def ig(update: Update, context: CallbackContext):
    text = update.message.text[4:]
    # if update.message.text[:3] == '/ig':
    #     text = update.message.text[4:]
    if text == '':
        context.bot.send_message(chat_id=update.message.chat_id, text='請貼上連結 >w<')
        return
    context.bot.send_message(chat_id=update.message.chat_id, text='下載中...')

    wb = webdriver.Chrome()
    # driver = webdriver.Remote(service.service_url)
    wb.get(text)
    try:
        WebDriverWait(wb, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_aagv')))
    finally:
        pass

    imgLink = []
    try:
        while True:
            sleep(1)
            imgLink.append(get_xpath_attribute(wb, '//div[@class="_aagv"]/img', 'src'))
            wb.find_element(By.XPATH, '//button[@class=" _afxw"]').click()
    except:
        pass


    n = len(imgLink)
    print(update)
    for i in range(len(imgLink)):
        print(imgLink[i])
        context.bot.send_photo(update.message.chat.id, photo=imgLink[i])
        # try:
        #     wb.get(imgLink[i])
        #     WebDriverWait(wb, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        # finally:
        #     pass
    wb.quit()   

from pytube import YouTube as Youtube
from pytube.cli import on_progress
import sys
# -*- coding:utf-8 -*-
def yt(update: Update, context: CallbackContext):
    url = update.message.text[4:]
    # targetPath = './mp3'
    targetPath = '.\\mp3'
    if url == '':
        context.bot.send_message(chat_id=update.message.chat_id, text='請貼上連結 >w<')
        return
    context.bot.send_message(chat_id=update.message.chat_id, text='下載中...')
    yt = Youtube(url,on_progress_callback=on_progress)
    # yt.streams.first().download(output_path=targetPath, filename=f'{yt.title}.mp3')
    filename = yt.streams.filter().get_audio_only().default_filename
    optpath = f'{targetPath}\\{filename}.mp3'
    yt.streams.filter().get_audio_only().download(output_path=targetPath, filename=f'{filename}.mp3')
    # yt.streams.filter(only_audio=True).get_highest_resolution().download(output_path=targetPath, filename=f'{yt.title}.mp3')
    context.bot.send_message(chat_id=update.message.chat_id, text='下載完畢')
    context.bot.send_message(chat_id=update.message.chat_id, text='上傳中...')
    # update.getUpdates(timeout=1000)
    # update.timeout = 1000
    # tt = telegram.utils.request.Request(connect_timeout=5, read_timeout=20, write_timeout=tt)
    # with open(optpath, 'rb') as f:
    #     context.bot.send_file(chat_id=update.message.chat.id, audio=f, write_timeout=20)
    context.bot.send_document(chat_id=update.message.chat.id, document=open(f'{optpath}', 'rb'), timeout=1000)
    # context.bot.send_audio(chat_id=update.message.chat.id, audio=open(f'{optpath}', 'rb'))
    context.bot.send_message(chat_id=update.message.chat_id, text='上傳完畢')