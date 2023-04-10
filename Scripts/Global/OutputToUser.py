'''
    # Output functions to print/tell user
'''

import os
import sys
import traceback
import datetime
import pytz
import inspect
from telegram import *
from telegram.ext import *
from typing import *

from Scripts.Telegram.values import updater
from Scripts.Global.JSON_Handler import CJson
from Scripts.Global.HTML_Formatter import bold, code


def get_params(function):
    '''## get the parameters of a function/method'''
    return list(inspect.signature(function).parameters.keys())


def send_user(*args,
              method=updater.bot.send_message,
              pm: bool = False,
              wpp: bool = False,
              reply: Message = None,
              **kwargs):
    '''
        ## send messages (text/media) easier
        - `pm=True` for `'parse_mode'='html'`
        - `wpp=True` for `'disable_web_page_preview'=True`
        - `reply=Message` to reply to that message
        - automatically applies `allow_sending_without_reply` if argument exists
    '''
    if pm:
        kwargs.setdefault('parse_mode', 'html')
    if wpp:
        kwargs.setdefault('disable_web_page_preview', True)
    if reply:
        kwargs.setdefault('reply_to_message_id', reply.message_id)
    if 'allow_sending_without_reply' in get_params(method):
        kwargs.setdefault('allow_sending_without_reply', True)

    return method(*args, **kwargs)


def get_error():
    '''
        ## get the error text in a better format
    '''
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return CJson.get_text({
        'type': exc_type.__name__,
        'text': str(exc_obj),
        'file': os.path.split(exc_tb.tb_frame.f_code.co_filename)[1],
        'line': exc_tb.tb_lineno,
    })


def send_error(message: Message, **kwargs):
    '''
        ## sends error text to ther user
        - use `text` in kwargs to override the default text that is sent
        - use `message=None` to only print traceback
    '''
    traceback.print_exc()
    if message:
        try:
            kwargs.setdefault('text', code(get_error()))
            return send_user(message.chat_id, kwargs['text'],
                             pm=True, reply=message)
        except:
            traceback.print_exc()


def get_current_date(country: str = None):
    '''
        ## get the current date in a better format
        - use `country=COUNTRY_CODE` to return in the timezone of that country
        - default timezone: UTC
    '''
    if country:
        return str(datetime.datetime.now(pytz.timezone(country)))
    return datetime.datetime.utcnow().strftime("%d-%m-%Y~%H:%M:%S UTC")
