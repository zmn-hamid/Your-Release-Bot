'''# Inline handler: search'''

from telegram import *
from telegram.ext import *
from uuid import uuid4

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import UserDataHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code
from Scripts.Global.SpotifyHandler import SpotifyHandler, spot


def inline_handler(update: Update, context):
    '''
        # handler to search artist inline
    '''
    try:
        inq: InlineQuery = update.inline_query
        user_id = inq.from_user.id
        query = inq.query.strip()
        if not query:
            return

        results = []
        for result in spot.search(
            q=query,
            type='artist',
            limit=5,
        )['artists']['items']:
            # arguments for `InlineQueryResultArticle`
            kwargs = dict(
                id=uuid4(),
                title=result['name'],
                input_message_content=InputTextMessageContent(
                    SpotifyHandler.get_link(result)),
            )

            # number of followers as description
            try:
                if result.get('followers') and result['followers'].get('total'):
                    kwargs['description'] = result['followers']['total']
            except:
                pass

            # artist's image for thumbnail
            try:
                if result.get('images'):
                    kwargs['thumb_url'] = result['images'][-1]['url']
            except:
                pass

            # appending result
            results.append(InlineQueryResultArticle(**kwargs))

        if len(results):
            inq.answer(results)
    except Exception as e:
        try:
            print(f'inlineERR ({user_id}): {e}')
        except:
            send_error(None)


inline_handlers = [
    InlineQueryHandler(inline_handler)
]
