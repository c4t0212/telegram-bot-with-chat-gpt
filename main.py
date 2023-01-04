import openai
from fun import *
from telegram import *
from dotenv import load_dotenv

class TelegramBot():
    def __init__(self):
        load_dotenv()
        token = os.getenv('TOKEN')
        self.app = ApplicationBuilder().token(token).build()
        self.CommandHandlerName = ['start', 'img', 'yt']
        self.CallbackQueryHandlerName = ['get_img']
    
    def run(self):
        for fun in self.CommandHandlerName:
            self.app.add_handler(CommandHandler(fun, eval(fun)))
        for fun in self.CallbackQueryHandlerName:
            self.app.add_handler(CallbackQueryHandler(eval(fun)))

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.app.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()