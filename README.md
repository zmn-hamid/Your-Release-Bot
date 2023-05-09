# Your Release Bot (Telegram)

Get the latest releases of your Spotify artists with a single Telegram bot. It was up on @YourReleaseBot

#### Features

User features:

- Adding and deleting artists from your panel
- Checking your added artists
- Taking a backup of your artists
- Resetting your artists (sends backup too)
- Changing the language of the bot
- Inline searching for an artist's URL, as well as the command version
- Checking plan information
- [optional] Checking donation information

Admin features:

- Automatically fetching, sending and applying the new releases
- Getting a text/json of the users who started the bot
- Getting a json of a specific user's data
- Getting a json of the whole users' database
- Getting and setting a user's plan

General features:

- Automatically saving the users who start the bot to the starteds database
- Changing settings using glass buttons
- Getting help after you choose language after you start the bot
- Changing the language to many languages, but easier to choose for: English, Farsi (Persian), Russian, Turkish
- Double checking with user before resetting, also backing up and sending to the user
- Translating almost everything to the chosen language with Google Translator.
  Note: Has some problems when translating commands (help text is the most troubled)

## Getting Started

#### Prerequisites

python 3.10+ installed and added to the path.
my version: 3.11.2

### Installation

1. Open terminal in the root directory and install requirement with this command:
   ```
   pip install -r requirements.txt
   ```
2. Make your bot:
   1. Go to [Bot Father](https://t.me/BotFather)
   2. Create a new bot and copy your token.
   3. [optional] in the bot's settings, you can change inline placeholder to 'Artist Name...' and preferrably disable adding to groups.
3. Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), make a new app and in the settings, copy your Client ID and Client Secret.
4. We need the ID of admin. If you're the admin, you can send a message to [What's My Telegram ID](https://github.com/MasterGroosha/my-id-bot) to get your ID, then copy it. If you aren't the admin, send a message from admin to this bot.
   <b>Note</b>: Admin must have a username. Copy their username as well.
5. Clone the project
6. In the [Data](Data/) folder, put three files:
   - `database_file.json`:
   ```
   {
      "users": {},
      "artists": {}
   }
   ```
   - `starteds_db.json`:
   ```
   []
   ```
   - `file_ids.json`:
   ```
   {}
   ```
   You can put these three files anywhere under the main directory, but you have to address them correctly.
7. Make a `config.py` file in the root directory, and put this text inside it:

   ```
   BOT_TOKEN = 'Your Bot Token'

   SPOT_CLIENT_ID = 'Your Spotify App Client ID'
   SPOT_CLIENT_SECRET = 'Your Spotify App Client Secret'

   # [OPTIONAL]
   PRIVATE_CHAT_ID = ''  # starts with -100

   ADMIN_ID = 'The Chat ID Of Admin'
   ADMIN_USERNAME = 'The Username Of Admin'  # starts with @

   PLANS = {
      None: {'size': 80},  # free plan
      'A': {'size': 150},
      'B': {'size': 200},
      'C': {'size': 300},
      'D': {'size': 400},
      'E': {'size': 500},
   }

   SLEEP_TIME = 1.5  # recommended

   # [OPTIONAL]
   DONATION = {}  # example: 'Tether (TRC20)' : '...'

   DATA_FILE_PATH = 'path/to/database_file.json'
   STARTEDS_FILE_APTH = 'path/to/starteds_db.json'
   FILE_IDS = 'path/to/file_ids.json'

   VIDEO_TUTORIAL_PATH = ''  # path/to/video_tutorial.mp4
   VIDEO_TUTORIAL_CAPTION = ''  # example: '<b>Video Tutorial</b>'

   ```

   Additional Information:

   - `PRIVATE_CHAT_ID`: you can make a channel, send a message in it, then forward this message to that bot to get it's ID.
     <b>Note</b>: This bot returns correct, but if you used other ways to get the ID, you have to check if it has `-100` in the beginning, if not, add it.
   - `PLANS`: There must be a Free plan (the first row), but you can change its size as you want. The size is how many artists can the user with that plan, add.
   - `SLEEP_TIME`: The sleep time between each request to Spotify's server.
   - `DONATION`: If you don't want to add donation option, leave this be. But if you do, you can add the name of the donation option and the value/url to it, as a dict. You can put any HTML formatting too. Example:
     ```
     DONATION = {  # name, value
        'Tether (BEP20)': '<code>0xF11206c22...</code>',  # it's copiable
     }
     ```
   - `DATA_FILE_PATH`: It must be relative to the main directory. For example, if you did step 5 the exame same way, it'll be `Data/database_file.json`
   - `STARTEDS_FILE_APTH`: the same as `DATA_FILE_PATH`. It'll be `Data/starteds_db.json` by default.
   - `FILE_IDS`: the same as `DATA_FILE_PATH`. It'll be `Data/file_ids.json` by default.
   - `VIDEO_TUTORIAL_PATH`: You can put your tutorial video in [Data / Video](Data/Video/) and change this variable accordingly. If you leave it be empty, it won't send any video tutorial.
   - `VIDEO_TUTORIAL_CAPTION`: A HTML formatted text as the caption of the video tutorial.

#### Usage

Once you're in the root directory, run the app using `python bot.py`.

## License

MIT License

This project is free and open-source. You can use, modify, and distribute it without any restrictions.

## Contact

If you have any questions or feedback about this project, feel free to get in touch with me:

- Email: zmn-hamid@proton.me
- [Telegram](https://t.me/hamid1780)
- [GitHub Issues](https://github.com/zmn-hamid/spotify-full-album/issues)
