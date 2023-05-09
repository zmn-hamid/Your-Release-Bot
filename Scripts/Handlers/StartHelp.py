'''# Start and help command handler'''

from telegram import *
from telegram.ext import *

import config as CONFIG

from Scripts.Telegram.values import updater

from Scripts.Handlers.Global.InitialValues import user_data_init
from Scripts.Handlers.Global.UserHyperlink import user_hyperlink
from Scripts.Handlers.Global.HelpText import help_en
from Scripts.Handlers.Global.GetVideoTutorial import get_video_tutorial

from Scripts.Global.OutputToUser import send_user, send_error
from Scripts.Global.DatabaseHandler import UserDataHandler, StartedsHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.LanguageMarkup import language_reply_markup
from Scripts.Global.JSON_Handler import CJson


def start_command(update: Update, context):
    '''
        # handler for when user started
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id)

            # [OPTIONAL] add the user to the starteds
            try:
                (dbh_starteds := StartedsHandler()).add_user(user_id=user_id)
                dbh_starteds.save_database()
            except:
                pass

            # [OPTIONAL] log to private chat
            try:
                send_user(CONFIG.PRIVATE_CHAT_ID,
                          user_hyperlink(user_id=user_id), pm=True)
            except:
                pass

            # send user the language buttons
            # OPTION REMOVED
            # send_user(chat_id, bold(tr.do('Choose! (preferably english)')),
            #           reply_markup=language_reply_markup('', True),
            #           pm=True, reply=message)

            # send the help
            help_command(update=update, context=context)
        except:
            send_error(message=message)


def help_command(update: Update, context):
    '''
        # handler to send help text
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id)

            # send help text
            send_user(chat_id, tr.do(help_en),
                      pm=True, wpp=True, reply=message)

            # [OPTIONAL] send video tutorial
            try:
                file_id = None
                file_ids = None
                # try getting saved file id
                try:
                    file_ids = CJson.loads(CONFIG.FILE_IDS)
                    file_id = file_ids['video-tutorial']
                except:
                    pass

                default_kwargs = dict(
                    caption=CONFIG.VIDEO_TUTORIAL_CAPTION,
                    pm=True, reply=message, method=message.reply_video
                )

                if file_id:
                    send_user(file_id, **default_kwargs)
                else:
                    msg = send_user(open(get_video_tutorial(), 'rb'),
                                    **default_kwargs)
                    if not file_ids:
                        file_ids = {}
                    file_ids['video-tutorial'] = msg.video.file_id
                    CJson.dumps(file_ids, CONFIG.FILE_IDS)
            except:
                pass
        except:
            send_error(message=message)


start_help_handlers = [
    CommandHandler('start', start_command),
    CommandHandler('help', help_command),
]
