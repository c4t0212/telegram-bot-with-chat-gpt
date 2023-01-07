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


class TelegramBotFunction():
    def __init__(self):
        self.args = ''
    def start(self, update: Update, context: CallbackContext):
        msg = \
        """
        使用方法:
        圖片生成: /img [文字]
        IG貼文圖片抓取: /ig [IG網址]
        YT MP3下載: /yt [YT網址]
        """
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    def get_img(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.edit_message_text(text=f"生成中...")
        text = self.args
        imgNums = int(query.data)

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
        context.bot.send_media_group(update.callback_query.message.chat.id, media=[InputMediaPhoto(media=url['url']) for url in res['data']])
        context.dispatcher.remove_handler(CallbackQueryHandler(self.get_img))
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text='生成完畢 uwu',reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("重新生成", callback_data=query.data)]]))

    def img(self, update: Update, context: CallbackContext):
        self.args = 'img'
        context.bot.send_message(chat_id=update.message.chat_id, text='請輸入文字 uwu')
        context.dispatcher.add_handler(CallbackQueryHandler(self.get_img))
        context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.get_text))

    def get_text(self, update: Update, context: CallbackContext):
        context.dispatcher.remove_handler(MessageHandler(Filters.text & ~Filters.command, self.get_text))
        text = update.message.text

        if self.args == 'img':
            self.args = text
            inlineKeyboard = [[InlineKeyboardButton(str(_ * 4 + x), callback_data=_ * 4 + x) for x in range(1, 5)] for _ in range(2)]
            update.message.reply_text('選擇要生成幾張圖片', reply_markup=InlineKeyboardMarkup(inlineKeyboard, one_time_keyboard=True))
            return self.get_img
        elif self.args[:2] == 'yt':
            if self.args == 'ytv':
                self.args = '-' + text
            else:
                self.args = text
            return self.get_yt(update, context)
        return CommandHandler.end
    
    def get_res(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.edit_message_text(text=f"下載中...")
        context.dispatcher.remove_handler(CallbackQueryHandler(self.get_res))
        resolution = query.data + 'p'
        yt = self.args
        file = yt.streams.filter(res=resolution).first().title + '.mp4'
        yt.streams.filter(res=resolution).first().download(filename=file)
        context.bot.send_video(chat_id=update.callback_query.message.chat.id, video=open(file, 'rb'))
        os.remove(file)
        print(file)
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text='上傳完畢')

    def get_yt(self, update: Update, context: CallbackContext):
        msg = context.bot.send_message(chat_id=update.message.chat_id, text='下載中...')
        url = update.message.text
        yt = Youtube(url)
        # yt = Youtube(url,on_progress_callback=on_progress)
        file = ''
        if self.args[0] == '-':
            resolution = [int(i.split("p")[0]) for i in (list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution])))]
            resolution.sort()
            self.args = yt
            msg = context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text=f'選擇要下載的畫質\n', reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(str(x), callback_data=x) for x in resolution
            ]], one_time_keyboard=True))     
            return self.get_res
        
        file = yt.streams.filter().get_audio_only().title + '.mp3'
        yt.streams.filter(only_audio=True).first().download(filename=file)
        msg = context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text='上傳中...')
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(file, 'rb'))
        msg = context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=msg.message_id, text='上傳完畢')
        print(f'{file} file size: {yt.streams.filter().get_audio_only().filesize_mb} MB')
        os.remove(file)

    def yt_audio(self, update: Update, context: CallbackContext):
        self.args = 'yt'
        context.bot.send_message(chat_id=update.message.chat_id, text='請貼上連結 >w<')
        context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.get_text))

    def yt_video(self, update: Update, context: CallbackContext):
        self.args = 'ytv'
        context.bot.send_message(chat_id=update.message.chat_id, text='請貼上連結 >w<')
        context.dispatcher.add_handler(CallbackQueryHandler(self.get_yt))
        context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.get_text))

    def err(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id, text='發生錯誤，給東三一塊餅乾叫他加班 >w<')