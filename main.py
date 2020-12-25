import logging
import telebot
import cli

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

telebot.run()
#cli.run()