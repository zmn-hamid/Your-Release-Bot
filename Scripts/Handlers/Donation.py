'''# Donation handler'''

from telegram import *
from telegram.ext import *

import config as CONFIG

from Scripts.Handlers.Global.InitialValues import user_data_init

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code
from Scripts.Global.SpotifyHandler import SpotifyHandler, spot


def donation(update: Update, context):
    '''
        # handler to send donation information to user
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            send_user(chat_id, '%s :3\n\n%s\n Contact admin for more.' % (
                tr.do("Your donation helps me upgrade the bot as well"),
                '\n'.join(['%s: %s' % (name, value)
                          for name, value in CONFIG.DONATION.items()]),
            ), pm=True, reply=message)
        except:
            send_error(message=message)


donation_handlers = [
    CommandHandler('donation', donation),
] if CONFIG.DONATION else []  # check if donation is activated
