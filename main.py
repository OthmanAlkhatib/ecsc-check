from telegram.ext import CommandHandler, Updater, CallbackContext
from telegram import Update
import os
import logging
import sys
import threading

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


def check_ecsc():
    pass


def start_check_ecsc_thread():
    thread = threading.Thread(target=check_ecsc, args=())
    thread.daemon = True
    thread.start()



if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)

    run()
    start_check_ecsc_thread()