'''
    # Telegram bot's global values
'''

from telegram import *
from telegram.ext import *
import config as CREDS

updater = Updater(CREDS.BOT_TOKEN)
dispatcher = updater.dispatcher
BOT_USERNAME, BOT_ID = updater.bot.username, updater.bot.id
