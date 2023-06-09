'''
    # Initial values for handlers
'''

from telegram import *
from telegram.ext import *
from typing import *

from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.Translator import Translator


def user_data_init(user_id: str, message: Message = None):
    '''
        ## returns `dbh`, `tr`
    '''
    dbh = UserDataHandler()
    if message and not dbh.user_exists(user_id=user_id):
        # handle no/wrong user language code
        try:
            language_code = Translator.validate_language(
                language=message.from_user.language_code)
        except:
            language_code = 'en'

        dbh.create_user(user_id=user_id, user_plan=None,
                        user_language=language_code, user_artists=[])
    (tr := Translator()).set_language(
        dbh.get_language(user_id=user_id))
    dbh.save_database()

    return dbh, tr
