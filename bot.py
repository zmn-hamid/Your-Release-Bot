'''# Main script'''

from telegram import *
from telegram.ext import *

from Scripts.Telegram.values import (
    updater,
    dispatcher,
    BOT_USERNAME,
)

from Scripts.Handlers.Global.Commands import commands

# importing handlers
from Scripts.Handlers.AddArtist import add_artists_handlers
from Scripts.Handlers.Admin import admin_handlers
from Scripts.Handlers.DelArtist import del_artists_handlers
from Scripts.Handlers.Donation import donation_handlers
from Scripts.Handlers.Inline import inline_handlers
from Scripts.Handlers.Language import language_handlers
from Scripts.Handlers.Search import search_handlers
from Scripts.Handlers.Settings import settings_handlers
from Scripts.Handlers.StartHelp import start_help_handlers


# adding the handlers
for handler in [
    *start_help_handlers,
    *admin_handlers,
    *donation_handlers,
    *inline_handlers,
    *search_handlers,
    *language_handlers,
    *settings_handlers,
    *del_artists_handlers,
    *add_artists_handlers,  # Filters.text is here
]:
    dispatcher.add_handler(handler)

# adding the commands
updater.bot.set_my_commands(commands)

# running the app
updater.start_polling()
print(f'polling {BOT_USERNAME}...')
updater.idle()
