'''# Delete artist handler'''

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


def del_artists_handler(update: Update, context):
    '''
        # handler to del artist from the user's data
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)
            artist_ids = message.text.split()

            # getting the iterator
            del_artists_iter = dbh.del_artists(
                user_id=user_id, artist_ids=artist_ids)

            # backing up the user's artists and database artists for possible failure
            backup_user_database = dbh.backup_database()

            # iterating the artists
            send_user(chat_id, tr.do(
                f'{len(artist_ids)} artist(s) detected...'), reply=message)
            for artist_idx, artist_perform in del_artists_iter:
                try:
                    # performing the operation
                    artist = artist_perform()
                    send_user(chat_id, bold('%s "%s"' % (
                        tr.do("Detected"), hyperlink(
                            SpotifyHandler.get_link(artist), artist['name'])
                    )), pm=True, reply=message)
                except YRE.CouldntGetArtist as e:
                    send_user(chat_id, tr.do(
                        "Couldn't get artist") + ': ' + str(e), wpp=True, reply=message)
                    continue
                except YRE.ArtistNotAdded as e:
                    send_user(chat_id, tr.do(
                        "It's not added at all added: ") + str(e), reply=message)
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


del_artists_handlers = [
    CommandHandler('del', del_artists_handler),
]
