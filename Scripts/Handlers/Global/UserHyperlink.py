'''
    # Hyperlink text to user
'''

from Scripts.Telegram.values import updater

from Scripts.Global.HTML_Formatter import hyperlink


def user_hyperlink(user_id: str):
    '''
        ## returns a hyperlink text to the user's chat
    '''
    name, username = '', None
    try:
        user = updater.bot.get_chat(
            user_id).to_dict()
        name = ('%s %s' % (user.get('first_name', ''),
                           user.get('last_name', ''))).strip()
        username = user.get('username')
    except:
        pass
    name = name if name else 'NOT_FOUND_%s' % user_id

    return (hyperlink('https://t.me/%s' % username, name) if username
            else hyperlink('tg://user?id=%s' % user_id, name))
