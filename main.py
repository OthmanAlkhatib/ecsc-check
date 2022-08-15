from telegram.ext import CommandHandler, Updater, CallbackContext, MessageHandler, Filters
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


ml = Melden()
updater = Updater(TOKEN)


def send_message(update:Update, context:CallbackContext):
    update.message.reply_text(update.message.chat.id)

is_site_open = 0
is_site_closed = 0
def check_site_reply():
    global is_site_open, is_site_closed, updater, ml
    if not ml.checkSite("https://www.ecsc.gov.sy/"):
        print("closed")
        if not is_site_closed:
            updater.bot.sendMessage(chat_id='872679970', text='Site is Closed')
            print("closed")
            is_site_closed = 1
            is_site_open = 0
        return False
    else:
        print("open")
        if not is_site_open:
            updater.bot.sendMessage(chat_id='872679970', text='Site is Open')
            is_site_open = 1
            is_site_closed = 0
        return True


is_doc_open = 0
is_doc_closed = 0
def check_doc_reply():
    global is_doc_open, is_doc_closed, updater, ml
    if not ml.checkDocument():
        print("closed")
        if not is_doc_closed:
            updater.bot.sendMessage(chat_id='872679970', text='Unfortuinatly, Making Document is Closed Again')
            is_doc_closed = 1
            is_doc_open = 0
    else:
        print("open")
        if not is_doc_open:
            updater.bot.sendMessage(chat_id='872679970', text='Quickly! You Can Make Document')
            is_doc_open = 1
            is_doc_closed = 0


PERSONAL_NUMBER = os.getenv("PERSONAL_NUMBER")
PASSWORD = os.getenv("PASSWORD")
def check_ecsc():
    global updater, ml
    try:
        if check_site_reply():
            check_doc_reply()
        time.sleep(120)

    except Exception as error:
        print(error)
        updater.bot.sendMessage(chat_id='872679970', text=error)

    time.sleep(5)


def make_document(update:Update, context:CallbackContext):
    try:
        text = update.message.text.split(" ")
        personal_number = text[1]
        password = text[2]
    except Exception as error:
        updater.bot.sendMessage(chat_id='872679970', text='Incorrect Input')

    try:
        ml2 = Melden()
        ml2.checkSite("https://www.ecsc.gov.sy/")
        ml2.login(personal_number, password)
        ml2.checkDocument()
        ml2.makeDocument()
        updater.bot.sendMessage(chat_id='872679970', text='Document has been created')

    except Exception as error:
        print("=== ml2 error ===")
        print(error)
        updater.bot.sendMessage(chat_id='872679970', text='Sorry, Can not make document')


# def start_check_ecsc_thread():
#     thread = threading.Thread(target=check_ecsc, args=())
#     thread.daemon = True
#     thread.start()

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", send_message))
    updater.dispatcher.add_handler(CommandHandler("make", make_document))
    run()
    while True:
        if check_site_reply():
            ml.login(PERSONAL_NUMBER, PASSWORD)
            break
    while True:
        try:
            check_ecsc()
        except Exception as error:
            print(error)
    # start_check_ecsc_thread()