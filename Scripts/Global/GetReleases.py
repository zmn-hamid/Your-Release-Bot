'''
    # Get the new releases of artists
'''

import os
import traceback
from typing import *

from telegram import *
from telegram.ext import *

from Scripts.Telegram.values import updater

from Scripts.Global.JSON_Handler import CJson
from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.OutputToUser import send_user, send_error, get_current_date
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.SpotifyHandler import SpotifyHandler
from Scripts.Global.Translator import Translator


def _get_releases(message: Message):
    '''
        ### gets the new releases
        - better not to be used directly, but instead using `get_releases`
    '''
    # init
    dbh = UserDataHandler()
    dbh._validate_db()
    default_kwargs = dict(method=message.reply_text)

    # get data
    users_data = dbh.db['users']
    artists_data = dbh.db['artists']

    # get and send backup
    filename = CJson.dumps(dbh.backup_database(), '.temp-adminuserdata.json')
    send_user(open(filename, 'rb'), method=message.reply_document,
              caption='Backup Database - %s' % get_current_date(), pm=True)

    # delete unavailable users
    deleted_users = []
    for user_id in users_data.keys():
        # send test message
        try:
            test_message = send_user(user_id, 'test_message')
        except:
            deleted_users.append(user_id)
        # delete test message
        try:
            test_message.delete()
        except:
            pass
    for user_id in deleted_users:
        artists_data.pop(user_id)

    # {iterate in artists}
    # if artist not in any user: save as to-be-deleted
    # else: save as pending in this structure:
    # pending: {
    #     artist id: {
    #         artist info: {}
    #         releases: [
    #             {
    #                 type: [],
    #                 urls: [],
    #             },
    #             ...
    #         ]
    #     },
    #     ...
    # }
    removing_artists, pending = [], {}
    counter = 1
    msg = send_user('checking...', **default_kwargs)
    for artist_id, artist_data in artists_data.items():
        msg = send_user(bold('checking %s/%s' % (counter, len(artists_data))),
                        pm=True, method=msg.edit_text)
        counter += 1
        if artist_id not in [item for user_data in users_data.values() for item in user_data['artists']]:
            removing_artists.append(artist_id)
        else:
            artist_info = SpotifyHandler.get_albums(artist_id, show_first=7)
            # correct the artist's name
            artists_data[artist_id]['name'] = artist_info['name']
            # add pending
            for album in artist_info['albums']:
                # break if no new releases
                # if it fails, it may send 7 artists, that's why skipping feature is implemented later
                is_reached = False
                for url in album['urls']:
                    if url in artist_data['urls']:
                        is_reached = True
                        break
                if is_reached:
                    break

                if artist_id not in pending.keys():
                    pending[artist_id] = []
                pending[artist_id].append({
                    'urls': album['urls'],
                    'type': album['type'],
                    'artist_name': artist_info['name'],
                })
    send_user(bold(msg.text + ' [DONE]'), pm=True, method=msg.edit_text)

    # send the removing artists
    send_user('%s removing artist(s) detected:' % len(removing_artists),
              **default_kwargs)
    removing_artists_text = CJson.get_text(removing_artists)
    for idx in range(0, len(removing_artists_text), 4000):
        send_user(removing_artists_text[idx:idx+4000],
                  wpp=True, **default_kwargs)

    # send the pending artists
    send_user('%s pending artist(s) detected:' %
              len(pending), **default_kwargs)
    pending_text = CJson.get_text(pending)
    for idx in range(0, len(pending_text), 4000):
        send_user(pending_text[idx:idx+4000], wpp=True, **default_kwargs)

    # if no pending, send no pending
    if len(pending.items()) == 0:
        send_user('no new urls to send', **default_kwargs)

    # else, send pendings
    else:
        # send the urls, skip more than 7
        send_user('-- starting sending urls --', **default_kwargs)
        skipped = {}
        for user_id, user_data in users_data.items():
            for artist_id in user_data['artists']:
                if artist_id in pending.keys() and artist_id not in skipped.keys():
                    artist_pending_data = pending[artist_id]
                    if len(artist_pending_data) >= 7:
                        skipped[artist_id] = artist_pending_data
                    else:
                        for item in artist_pending_data:
                            try:
                                url = '\n'.join(item['urls'])
                                try:
                                    tr = Translator()
                                    tr.set_language(
                                        language=user_data.get('language', 'en'))
                                    send_user(
                                        user_id,
                                        tr.do(bold("artist: %s\ntype: %s\n%s") % (
                                            item['artist_name'], item['type'], url)),
                                        pm=True,
                                    )
                                    send_user(bold('+++ sent "%s" to "%s".' % (
                                        url, user_id)), pm=True, wpp=True,
                                        **default_kwargs)
                                except Exception as e:
                                    send_user('--- couldnt send "%s" to "%s" : %s' % (
                                        url, user_id, e))
                            except Exception as e:
                                send_user('--- couldnt send "%s" to "%s" :: %s' % (
                                    url, user_id, e))

        # send skips
        for artist_id, artists_urls_data in skipped.items():
            try:
                send_user(bold('!!! [ SKIP ] skipping %s (%s)' % (
                    artist_id, artists_urls_data[0]["artist"])),
                    pm=True, **default_kwargs)
            except:
                send_user('bruv !!! [ SKIP ] skipping %s' % artist_id,
                          pm=True, **default_kwargs)

        # send finished sending
        send_user('-- finished sending urls --', **default_kwargs)

    # remove, update urls, save database
    try:
        for artist_id in removing_artists:
            artists_data.pop(artist_id)
        for artist_id, data in pending.items():
            artists_data[artist_id]['urls'] = data[0]['urls']
        dbh.save_database()
        send_user('-- finished saving database --', **default_kwargs)
    except Exception as e:
        send_error(message=message)

        # backup removing
        try:
            removing_artists_backup = CJson.dumps(
                removing_artists, 'ERR_REMOVING_ARTISTS')
            send_user(open(removing_artists_backup, 'rb'),
                      method=message.reply_document)
            os.remove(removing_artists_backup)
        except:
            traceback.print_exc()

        # backup pending
        try:
            pending_backup = CJson.dumps(pending, 'ERR_REMOVING_ARTISTS')
            send_user(open(pending_backup, 'rb'),
                      method=message.reply_document)
            os.remove(pending_backup)
        except:
            traceback.print_exc()


def get_releases(chat_id: str | int):
    '''
        ## Gets the new releases of spotify artists
        - `chat_id` can be anything
    '''
    message = updater.bot.send_message(chat_id, '- start -')
    message.from_user.id = int(chat_id)
    message.from_user.is_bot = False

    _get_releases(message=message)

    message = send_user(chat_id, '- end -')
