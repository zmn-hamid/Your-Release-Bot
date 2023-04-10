'''# Language handler'''

import re
from telegram import *
from telegram.ext import *
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as LANGS

from Scripts.Handlers.Global.InitialValues import user_data_init

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code
from Scripts.Global.LanguageMarkup import language_reply_markup

from Scripts.Handlers.StartHelp import help_command


def language(update: Update, context):
    '''
        # handler to manage user's language
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            if len(text := message.text.split(maxsplit=1)) == 2:
                # language manually entered
                chosen_lang = text[1].lower()
                try:
                    dbh.set_language(user_id=user_id, new_language=chosen_lang)
                    dbh.save_database()
                    tr.set_language(language=chosen_lang)
                    send_user(chat_id, tr.do(
                        f'language changed to {chosen_lang}'), reply=message)
                except YRE.WrongLanguage:
                    send_user(chat_id, tr.do(
                        'wrong country. use') + ' /language_other', reply=message)
            else:
                # sending glass buttons
                send_user(chat_id, bold(
                    tr.do('Choose! (preferably english)\n\nother languages: /other_languages')),
                    reply_markup=language_reply_markup(
                        chosen_language=tr.get_language(), start=False),
                    pm=True, reply=message)
        except:
            send_error(message=message)


def language_callback(update: Update, context):
    '''
        # handler language button callback
    '''
    if (message := (clbk := update.callback_query).message) and (
            user_id := clbk.from_user.id) and (
            chat_id := message.chat_id):
        data = [item for item in clbk.data.split('|')[1:] if item]
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            new_language = data[0]
            dbh.set_language(user_id=user_id, new_language=new_language)
            dbh.save_database()
            tr.set_language(language=new_language)

            send_user(bold(tr.do(
                'Choose! (preferably english)\n\nother languages: /language_other')),
                reply_markup=language_reply_markup(chosen_language=new_language,
                                                   start=False),
                pm=True, method=message.edit_text
            )

            if len(data) > 1 and data[1] == 'start' and message.reply_to_message:
                update.message = message.reply_to_message
                help_command(update, context)
        except:
            send_error(message=message)


def other_languages(update: Update, context):
    '''
        # handler to see other languages
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            text = '%s %s\n%s\n%s\n%s\n%s\n\n\n%s\n' % (
                tr.do("send other languages in this format:"),
                code("/language NAME"),
                tr.do("exmaple:"),
                code("/language english"),
                tr.do("or"),
                code("/language en"),
                tr.do("supported languages:")
            )
            text += '\n'.join([
                '%s (%s)' % (country, country_short)
                for country, country_short in LANGS.items()])
            send_user(chat_id, text, pm=True, reply=message)
        except:
            send_error(message=message)


language_handlers = [
    CommandHandler('language', language),
    CallbackQueryHandler(language_callback, pattern='^' +
                         re.escape('language|')),
    CommandHandler('other_languages', other_languages),
]
