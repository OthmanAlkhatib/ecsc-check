from telegram.ext import CommandHandler, Updater, CallbackContext
from telegram import Update
import os
import logging
import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from meden import Melden
import time

TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if MODE == "dev":
    def run():
        logger.info("Start in DEV mode")
        updater.start_polling()
elif MODE == "prod":
    def run():
        logger.info("Start in PROD mode")
        updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path=TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format("ecsc-check", TOKEN))
else:
    logger.error("No mode specified")
    sys.exit(1)


def send_message(update:Update, context:CallbackContext):
    update.message.reply_text(update.message.chat.id)

def check_ecsc():
    updater = Updater(TOKEN)
    ml = Melden()
    for i in range(3):
        if ml.checkSite():
            updater.bot.sendMessage(chat_id='872679970', text='Hello there!, Go sign up')
        else:
            updater.bot.sendMessage(chat_id='872679970', text='Sorry, but there is no place')

    # op = webdriver.ChromeOptions()
    # op.add_argument("headless")
    # while True:
    #     driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=op)
    #     driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng/ad889662-ea23-4531-ace3-1f1564c62f71;jsessionid=RniDnAVxpXktXVxtF_mceXWtDg0zFg0wPAiqzEM6.frontend-2?dswid=2275&dsrid=668&st=2&v=1659631472533")
    #     updater = Updater(TOKEN)
    #     updater.bot.sendMessage(chat_id='872679970', text='Hello there!')



def start_check_ecsc_thread():
    thread = threading.Thread(target=check_ecsc, args=())
    thread.daemon = True
    thread.start()



if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", send_message))
    run()
    start_check_ecsc_thread()