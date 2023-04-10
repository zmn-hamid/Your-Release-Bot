'''# Search handler'''

from telegram import *
from telegram.ext import *
from typing import *

from Scripts.Handlers.Global.InitialValues import user_data_init

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import DatabaseHandler, UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.SpotifyHandler import SpotifyHandler, spot


def search_command(update: Update, context):
    '''
        # handler to seach for artist
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id, message=message)

            # getting query
            query: list = message.text.split(maxsplit=1)
            if len(query) == 1:
                return send_user(chat_id, tr.do('wrong format. use') + ' /help',
                                 reply=message)
            query: str = query[1]

            # generating output
            output = []
            for result in spot.search(
                q=query,
                limit=5,
                type='artist',
            )['artists']['items']:
                text = '%s: %s' % (tr.do("name"), result["name"])
                if (
                    'followers' in result.keys() and
                    result['followers'] and
                    'total' in result['followers'].keys() and
                    result['followers']['total']
                ):
                    text += '\n%s: %s' % (
                        tr.do('number of followers'),
                        result['followers']['total']
                    )
                output.append(text + '\n%s: %s' % (
                    tr.do('url'), SpotifyHandler.get_link(result)))

            send_user(chat_id, f'\n{15*"-"}\n'.join(output),
                      wpp=True, reply=message)
        except:
            send_error(message)


search_handlers = [
    CommandHandler('search', search_command),
]
