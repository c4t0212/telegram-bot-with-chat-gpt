import logging
import os
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv
from fun import *
import requests as req

def set_command(funName  : list):
        handler = []
        ii = ['i', 'I', 'p', 'P', 'img']
        tt = ['t', 'T', 'x', 'txt']
        for i in ii:
            handler.append(CommandHandler(i, img))
        for i in tt:
            handler.append(CommandHandler(i, txt))
        for fun in funName:
            handler.append(CommandHandler(fun, eval(fun)))
        for hd in handler:
            dispatcher.add_handler(hd)
        updater.dispatcher.add_handler(CallbackQueryHandler(get_img))

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')
    set_header()
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    funName = ['start', 'test', 'ig', 'yt']
    set_command(funName)
    updater.start_polling()
    updater.idle()