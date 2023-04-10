'''
    # Keyboard markup for language option
'''

from telegram import *


def language_reply_markup(chosen_language: str, start: bool = False):
    '''
        ## base for language options's keyboard markup
        - <b>Note</b>: use `start` in the start command handler,
            to send the help text after the choosing of language
    '''
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                ('✅' if chosen_language in [
                 'en', 'english'] else '') + 'English🇺🇸',
                callback_data='language|english|'+('start' if start else '')),
            InlineKeyboardButton(
                ('✅' if chosen_language in [
                 'fa', 'persian'] else '') + 'فارسی🇮🇷',
                callback_data='language|persian|'+('start' if start else '')),
        ],
        [
            InlineKeyboardButton(
                ('✅' if chosen_language in [
                 'ru', 'russian'] else '') + 'Русский🇷🇺',
                callback_data='language|russian|'+('start' if start else '')),
            InlineKeyboardButton(
                ('✅' if chosen_language in [
                 'tr', 'turkish'] else '') + 'Türk🇹🇷',
                callback_data='language|turkish|'+('start' if start else '')),
        ],
    ])
