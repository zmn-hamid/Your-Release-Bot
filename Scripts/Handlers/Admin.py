'''
    # Admin handler
'''

from shlex import shlex
from telegram import *
from telegram.ext import *

import config as CONFIG

from Scripts.Telegram.values import updater

from Scripts.Handlers.Global.InitialValues import user_data_init
from Scripts.Handlers.Global.UserHyperlink import user_hyperlink

from Scripts.Global.OutputToUser import send_user, send_error, get_current_date
from Scripts.Global.DatabaseHandler import UserDataHandler, StartedsHandler
from Scripts.Global.Translator import Translator
from Scripts.Global.YR_Exceptions import YRE, YR_Exceptions
from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Global.JSON_Handler import CJson

from Scripts.Global.GetReleases import get_releases


def admin(update: Update, context, **kwargs):
    '''
        # handler to manage admin
    '''
    if (message := update.message) and (
            user_id := message.from_user.id) and (
            chat_id := message.chat_id):
        try:
            # init
            dbh, tr = user_data_init(user_id=user_id)

            if str(user_id) == CONFIG.ADMIN_ID:  # is admin
                sample_text = code('/admin %s') + ' : %s\n'
                help_text = ''.join([
                    sample_text % ('starteds text',
                                   'send started users as text'),
                    sample_text % ('starteds json',
                                   'send started users as js'),
                    '\n',
                    sample_text % ('rls',
                                   'send new releases'),
                    '\n',
                    sample_text % ('vip',
                                   'get help about vip'),
                    sample_text % ('vip get USER_ID',
                                   'get one user\'s plan'),
                    sample_text % ('vip set USER_ID PLAN_NAME',
                                   'set one user\'s plan'),
                    '\n',
                    sample_text % ('usersdata USER_ID',
                                   'send json of one user'),
                    '\n',
                    sample_text % ('datafile',
                                   'send the whole datafile as json'),
                ])

                textsplit = message.text
                if textsplit == '/admin':
                    return send_user(chat_id, help_text,
                                     pm=True, reply=message)
                textsplit = list(shlex(textsplit.split(' ', 1)[1]))

                match textsplit[0]:
                    case 'starteds':
                        match textsplit[1]:
                            case 'json':
                                send_user(open('user_data/YR_starteds.json', 'rb'),
                                          reply=message, method=message.reply_document,
                                          caption=bold(get_current_date()), pm=True)

                            case 'text':
                                for user_id in StartedsHandler().backup_database():
                                    send_user(chat_id,
                                              user_hyperlink(user_id=user_id),
                                              pm=True, reply=message)
                                send_user(chat_id, 'done', reply=message)

                    case 'vip':
                        if len(textsplit) == 1:
                            send_user(chat_id, '\n'.join(
                                ['%s -> %s' % (key, value['size'])
                                 for key, value in CONFIG.PLANS.items()]
                            ), reply=message)

                        else:
                            chosen_user_id = textsplit[2]
                            match textsplit[1]:
                                case 'get':
                                    send_user(chat_id, dbh.get_plan(
                                        user_id=chosen_user_id), reply=message)
                                case 'set':
                                    plan = textsplit[3]
                                    if plan == 'null':
                                        plan = None
                                    if plan not in list(CONFIG.PLANS.keys()):
                                        raise YRE.PlanDoesntExist(plan)
                                    dbh.set_plan(user_id=chosen_user_id,
                                                 new_plan=plan)
                                    dbh.save_database()
                                    send_user(chat_id, 'done', reply=message)

                    case 'rls':
                        get_releases(CONFIG.ADMIN_ID)

                    case 'usersdata':
                        chosen_user_id = textsplit[1]
                        filename = CJson.dumps(dbh.user_data(
                            user_id=chosen_user_id), '.temp-adminuserdata.json')
                        send_user(open(filename, 'rb'),
                                  method=message.reply_document,
                                  caption='%s - %s' % (code(chosen_user_id),
                                                       get_current_date()),
                                  pm=True, reply=message)

                    case 'datafile':
                        send_user(open('user_data/YR_data.json', 'rb'),
                                  method=message.reply_document,
                                  caption=bold(
                                      'datafile - '+get_current_date()),
                                  pm=True, reply=message)
            else:
                send_user(chat_id, tr.do("you ain't admin bro"), reply=message)
        except:
            send_error(message=message)


admin_handlers = [
    CommandHandler('admin', admin),
]
