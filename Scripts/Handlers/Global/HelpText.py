'''
    # Help text in english
'''

import config as CONFIG

from Scripts.Global.HTML_Formatter import bold, code, hyperlink
from Scripts.Telegram.values import BOT_USERNAME


new_line = '\n'
help_en = f'''
🤍 {bold("With this bot you can get the releases of your favorite musicians(bands/etc) the day they're released!")}

-----------------------
🟡 {bold("HOW TO USE THE BOT")}{new_line+"notice: video tutorial is also available under this message." if CONFIG.VIDEO_TUTORIAL_PATH else ''}
▫️ {bold("Step 1)")} Send your artist's Spotify URL (/id/URI). You can use inline mode or /search command to search too.
      note: You can send multiple artists in one message. If you wanna add multiple artists, please consider sending them together.
▫️ {bold("Step 2)")} If you need to delete an artist, use /del. Send /settings to check your artists/etc.
▫️ {bold("Step 3)")} You'll receive the new releases nearly each day if your artists release anything

-----------------------
🟠 {bold("command")}: /settings
▫️ {bold("usage")}: {code("/settings")}
▫️ {bold("options")}:
      {bold("Backup")}: to get a backup of your artists. you can copy the content and send it again to get your artists back.
      {bold("Resetting")}: to reset your artists to zero. Don't worry, it'll double ask you before deletion and sends backup too.
      {bold("Your Added Artists")}: to check your added artists
      {bold("Your Plan")}: to check your plan and see how many arists you can add. Contact admin to upgrade: @hamid1780
      {bold("language")}: to change your the language of bot (🇺🇸🇮🇷🇷🇺🇹🇷...)
            Note: You can use /language instead. Same thing.

-----------------------
🟠 {bold("command")}: /del
▫️ {bold("usage")}: {code("/del `ARTIST_LINK`")}
      replace `ARTIST_LINK` with the spotify link of your added artist
▫️ {bold("example")}: {code("/del https://open.spotify.com/artist/042mLfOBpH8OoX8A6sUYhf")}
▫️ {bold("description")}: This command is used to delete an artist you added.
      you can also find it with /settings -> Your Added Artists

-----------------------
🟠 {bold("command")}: /search
▫️ {bold("usage")}: {code("/search `ARTIST_NAME`")}
      replace `ARTIST_NAME` with the spotify name of your artist
▫️ {bold("example")}: {code("/search GHOST DATA")}
▫️ {bold("description")}: This command is used to search for an artist and give you its name.
      you can instead use {bold("inline mode")} like this: {bold(code(f"@{BOT_USERNAME} `ARTIST_NAME`"))}

-----------------------
🟠 {bold("command")}: /donation
▫️ {bold("description")}: Buy me a coffee with this command :3
      Your donation helps me upgrade the bot as well.

-----------------------
🤍 for any help, contact me
admin: {CONFIG.ADMIN_USERNAME}
my bots and news channel: @HamidBots
'''
