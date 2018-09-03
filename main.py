from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

updater = Updater(token=constants.token)

dispatcher = updater.dispatcher


def echo(bot, update):
    update.message.reply_text(update.message.text)


def main():

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()


if __name__ == '__main__':
    main()
