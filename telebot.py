from logic import logicbot

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


def echo(update: Update, context: CallbackContext) -> None:
    response = logicbot.get_response(update.message.text).text
    update.message.reply_text(response)
    print("User asks: " + update.message.text)
    print("Bot answers: " + response)


def run():
    updater = Updater("1496038489:AAGYjydE7x29F8rBTCB4kMKKM7oXvDy6ylE", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling(clean=True)

    print("Telegram bot is running!")

    updater.idle()

