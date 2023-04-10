'''
    # Formats the text with HTML tags
'''


def code(text: str):
    '''## `<code>` text'''
    return '<code>%s</code>' % text


def bold(text: str):
    '''## `<bold>` text'''
    return '<b>%s</b>' % text


def hyperlink(url: str, text: str):
    '''## `<a>` text'''
    return '<a href="%s">%s</a>' % (url, text)
