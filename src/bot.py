import logging
import requests
from src import lastfm

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from src.secret import TELEGRAM_TOKEN, LAST_FM_API_KEY


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def login(bot, update, args):
    req = requests.get('https://www.last.fm/api/auth?api_key={}'.format(LAST_FM_API_KEY)).json()


def test_draw(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text='Wait, analysing')
    file = lastfm.main('-u hey_canada -l 2')
    bot.send_message(chat_id=update.message.chat_id, text='Filename: {}'.format(file))
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(file, 'rb'))


if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps, pass_args=True)
    dispatcher.add_handler(caps_handler)

    test_handler = CommandHandler('test', test_draw, pass_args=True)
    dispatcher.add_handler(test_handler)
