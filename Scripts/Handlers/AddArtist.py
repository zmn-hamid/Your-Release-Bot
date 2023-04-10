'''# Add artist handler'''

from telegram import *
from telegram.ext import *
from typing import *

from Scripts.Handlers.Global.InitialValues import user_data_init

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import DatabaseHandler, UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.SpotifyHandler import SpotifyHandler


def add_artists_handler(update: Update, context):
    '''
        # handler to add artist to the user's data
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)
            artist_ids = message.text.split()

            # getting the iterator
            try:
                add_artists_iter = dbh.add_artists(
                    user_id=user_id, artist_ids=artist_ids)
            except YRE.UserPlanExceeded as e:
                return send_user(chat_id, tr.do(str(
                    'You\'ve exceeded your limit by %s artist(s). '
                    'Delete one artist or upgrade your plan.'
                ) % e), reply=message)
            except YRE.UserPlanWouldExceed as e:
                return send_user(chat_id, tr.do(str(
                    'You would exceed your limit by %s artist(s). '
                    'Reduce your artists or upgrade your plan.'
                ) % e), reply=message)

            # backing up the user's artists and database artists for possible failure
            backup_user_database = dbh.backup_database()

            # iterating the artists
            send_user(chat_id, tr.do(
                f'{len(artist_ids)} artist(s) detected...'), reply=message)
            for artist_idx, artist_perform in add_artists_iter:
                try:
                    # performing the operation
                    artist = artist_perform()
                    msg = send_user(chat_id, bold('%s "%s"' % (
                        tr.do("Detected"), hyperlink(
                            SpotifyHandler.get_link(artist), artist['name'])
                    )), pm=True, reply=message)
                except YRE.CouldntGetArtist as e:
                    msg = send_user(chat_id, tr.do(
                        "Couldn't get artist") + ': ' + str(e), wpp=True, reply=message)
                    continue
                except YRE.ArtistAlreadyAdded as e:
                    msg = send_user(chat_id, tr.do(
                        "It's already added: ") + str(e), reply=message)
                    continue

            try:
                dbh.save_database()
                return send_user(chat_id, bold(
                    '-- %s --' % (tr.do('Added the correct ones successfully.'))),
                    pm=True, reply=message)
            except:
                dbh.reset_database(backup_database=backup_user_database)
                dbh.save_database_no_fail()
                send_error(message=message)
            send_user(chat_id, tr.do('Nothing changed.'), reply=message)
        except:
            send_error(message=message)


add_artists_handlers = [
    MessageHandler(Filters.text, add_artists_handler)
]
