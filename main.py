import openai
from fun import *
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv

class TelegramBot():
    def __init__(self):
        load_dotenv()
        token = os.getenv('TOKEN')
        self.app = Updater(token=token, use_context=True, base_url=os.getenv('BASE_URL'))
        # self.app = Updater(token=token, use_context=True)
        self.CommandHandlerName = ['start', 'img', 'yt']
        self.CallbackQueryHandlerName = ['get_img']
        self.func = TelegramBotFunction()
    
    def run(self):
        for fun in self.CommandHandlerName:
            self.app.dispatcher.add_handler(CommandHandler(fun, eval('self.func.' + fun)))
        for fun in self.CallbackQueryHandlerName:
            self.app.dispatcher.add_handler(CallbackQueryHandler(eval('self.func.' + fun)))
        # self.app.dispatcher.add_handler(ErrorHandler(error, error_callback))
        self.app.dispatcher.add_error_handler(self.func.err)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.app.start_polling()
        self.app.idle()

if __name__ == '__main__':
    bot = TelegramBot()
    # bot.app.bot.logOut()
    bot.run()