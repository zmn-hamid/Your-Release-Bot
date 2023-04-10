'''# Settings handler'''

import re
import os
import time
import datetime
from telegram import *
from telegram.ext import *

import config as CONFIG

from Scripts.Telegram.values import updater

from Scripts.Handlers.Global.InitialValues import user_data_init

from Scripts.Global.OutputToUser import send_user, send_error, get_current_date
from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.SpotifyHandler import SpotifyHandler
from Scripts.Global.JSON_Handler import CJson


def settings(update: Update, context):
    '''
        # handler to manage user's settings
        - features: backup, reset, added artists, plan, language
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            send_user(chat_id, bold(tr.do('Choose:')), reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        tr.do('Backup'), callback_data='settings|backup|'),
                    InlineKeyboardButton(
                        tr.do('Resetting'), callback_data='settings|reset|'),
                ],
                [
                    InlineKeyboardButton(
                        tr.do('Your Added Artists'), callback_data='settings|your-artists|'),
                ],
                [
                    InlineKeyboardButton(
                        tr.do('Your Plan'), callback_data='settings|your-plan|'),
                    # used in /language but publicly accessed here
                    InlineKeyboardButton(
                        tr.do('Language'), callback_data='language|%s' % tr.get_language()),
                ],
            ]), pm=True, reply=message)
        except:
            send_error(message)


BACKUP_FOLDER = 'Backup'


def delete_user_backups(user_id: str, minutes: int = 3):
    '''
        ## deletes the backups of user
        - if `minutes` has passed, deletes those files
        ### not a handler
    '''
    for _file in os.listdir(BACKUP_FOLDER):
        result = re.search(
            fr'backup-{user_id}-(\d+\.\d+)\.json', _file)
        if result:
            timestamp = float(result.groups()[0])
            if abs(
                datetime.datetime.fromtimestamp(timestamp) -
                datetime.datetime.now()
            ) > abs(datetime.timedelta(minutes=5)):
                os.remove('%s/%s' % (BACKUP_FOLDER, result.group()))


def backup_callback(update: Update, context):
    '''
        # handler for backup button callback
    '''
    if (message := (clbk := update.callback_query).message) and (
            user_id := clbk.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # no more needed / preventing from resending
            message.delete()

            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            # backing up
            delete_user_backups(user_id=user_id)
            user_data = dbh.user_data(user_id=user_id)
            backup_file = CJson.dumps(
                user_data['artists'],
                '%s/backup-%s-%s.json' % (BACKUP_FOLDER, user_id, time.time())
            )

            # sending to user
            send_user(chat_id, open(backup_file, 'rb'), caption=bold(tr.do(
                f'backed up at %s\ndont change the file' % get_current_date())),
                reply=message.reply_to_message, method=updater.bot.send_document,
                pm=True)
        except:
            send_error(message=message)


def reset_callback(update: Update, context):
    '''
        # handler for reset button callback
    '''
    if (message := (clbk := update.callback_query).message) and (
            user_id := clbk.from_user.id) and (
            chat_id := message.chat_id):
        data = [item for item in clbk.data.split('|')[1:] if item]
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            if len(data) == 1:
                if not len(dbh.user_data(user_id=user_id)['artists']):
                    send_user(message, tr.do('you dont have any artists at all.'),
                              method=message.edit_text)
                else:
                    send_user(
                        message, bold(tr.do('You sure?')),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(
                                tr.do("Yeah I'm sure"),
                                callback_data='settings|reset|first-approval')],
                            [InlineKeyboardButton(
                                tr.do("No, Don't reset"),
                                callback_data='settings|reset|cancel')],
                        ]), pm=True, method=message.edit_text)

            else:
                match data[1]:
                    case 'first-approval':
                        send_user(
                            message, bold(tr.do('%100 sure?')),
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton(
                                    tr.do("Yes."),
                                    callback_data='settings|reset|second-approval')],
                                [InlineKeyboardButton(
                                    tr.do("No No..."),
                                    callback_data='settings|reset|cancel')],
                            ]), pm=True, method=message.edit_text)

                    case 'second-approval':
                        # no more needed / preventing from resending
                        message.delete()

                        # backing up
                        delete_user_backups(user_id=user_id)
                        user_data = dbh.user_data(
                            user_id=user_id, message=message)
                        backup_file = CJson.dumps(
                            user_data['artists'],
                            '%s/backup-%s-%s.json' % (BACKUP_FOLDER,
                                                      user_id, time.time()))

                        # sending backup to user
                        send_user(chat_id, open(backup_file, 'rb'), caption=bold(tr.do(
                            f'backed up at %s\ndont change the file' % get_current_date())),
                            reply=message.reply_to_message, method=updater.bot.send_document,
                            pm=True)

                        # reset user
                        dbh.reset_user_artists(user_id=user_id, artist_ids=[])
                        dbh.save_database()
                        send_user(chat_id,
                                  bold('-- %s --' %
                                       (tr.do('reset successfully.'))),
                                  reply=message.reply_to_message, pm=True)

                    case 'cancel':
                        send_user(message, tr.do("Didn't reset anything."),
                                  method=message.edit_text)
        except:
            send_error(message=message)


def your_artists_callback(update: Update, context):
    '''
        # handler for your added artists button callback
    '''
    if (message := (clbk := update.callback_query).message) and (
            user_id := clbk.from_user.id) and (
            chat_id := message.chat_id):
        data = [item for item in clbk.data.split('|')[1:] if item]
        try:
            # no more needed / preventing from resending
            message.delete()

            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            if len(data) == 1:
                if user_artists := dbh.user_data(user_id=user_id)['artists']:
                    send_user(chat_id, bold(
                        tr.do('You have %s artist(s):' % len(user_artists))),
                        pm=True, reply=message.reply_to_message)

                    text = ''
                    for idx, artist_id in enumerate(user_artists):
                        text += '+ %s\n' % hyperlink(
                            artist_id, dbh.artists_data().get(
                                artist_id, {}).get('name', 'NO_NAME_FOUND'))
                        if idx == 100 or idx == len(user_artists) - 1:
                            send_user(chat_id, text, pm=True,
                                      wpp=True, reply=message.reply_to_message)
                            text = ''
                else:
                    send_user(chat_id, bold(tr.do(f'You have no artist yet.')),
                              method=message.edit_text, pm=True)
        except:
            send_error(message=message)


def your_plan_callback(update: Update, context):
    '''
        # handler for your plan button callback
    '''
    if (message := (clbk := update.callback_query).message) and (
            user_id := clbk.from_user.id) and (
            chat_id := message.chat_id):
        data = [item for item in clbk.data.split('|')[1:] if item]
        try:
            # no more needed / preventing from resending
            message.delete()

            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            output_list = []
            for plan_name, data in CONFIG.PLANS.items():
                flag = ''
                if plan_name == dbh.get_plan(user_id=user_id):
                    flag = ' [%s]' % tr.do('your plan')
                output_list.append('%s <b>%s</b>: %s %s%s' % (
                    tr.do('plan'), plan_name if plan_name else 'FREE',
                    data['size'], tr.do('artists'), flag))
            send_user(chat_id, ('\n%s\n' % (15*'-')).join(output_list) +
                      '\n\n%s.' % (tr.do("To upgrade contact admin")),
                      pm=True, reply=message.reply_to_message)
        except:
            send_error(message=message)


settings_handlers = [
    CommandHandler('settings', settings),
    CallbackQueryHandler(backup_callback, pattern='^' +
                         re.escape('settings|backup|')),
    CallbackQueryHandler(reset_callback, pattern='^' +
                         re.escape('settings|reset|')),
    CallbackQueryHandler(your_artists_callback, pattern='^' +
                         re.escape('settings|your-artists|')),
    CallbackQueryHandler(your_plan_callback, pattern='^' +
                         re.escape('settings|your-plan|')),
]
