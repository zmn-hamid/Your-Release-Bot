import config as CONFIG

commands = [
    ('help', 'get help'),
    ('del', 'delete artist'),
    ('search', 'search for artist'),
    ('language', 'change language'),
    ('settings', 'manage user settings'),
]

if CONFIG.DONATION:
    commands.append(('donation', 'donate developer'))
