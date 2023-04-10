'''
    # Handles any database
    - `UserDataHandler` and `StartedsHandler` are currently the main ones
'''


import time
from typing import *

import config as CONFIG

from Scripts.Global.YR_Exceptions import YRE
from Scripts.Global.SpotifyHandler import SpotifyHandler
from Scripts.Global.JSON_Handler import CJson
from Scripts.Global.HTML_Formatter import code, bold
from Scripts.Global.Translator import Translator


class ArtistPerformIterator:
    '''
        ## base for user artists operations
        - adding, deleting, etc\n

        ### inherit this class and override the `perform` method\n
        - use `self.index` to access the current item in `self.artist_ids`\n
    '''

    def __init__(self, db, user_id, artist_ids, user_artists) -> None:
        self.index = -1
        self.db = db
        self.user_id = user_id
        self.artist_ids = artist_ids
        self.user_artists = user_artists

    def __iter__(self):
        return self

    def perform(self):
        '''overrid this'''

    def __next__(self):
        self.index += 1
        if self.index >= len(self.artist_ids):
            raise StopIteration
        return self.index, self.perform


class DatabaseHandler:
    '''
        ## Handle fetching, validating, and saving the DB
        - inherit this class to handle your database
    '''

    def __init__(self,
                 **kwargs) -> None:
        self.db_path = None
        self.db = None
        self.backup_db = None

    def _validate_db(self,
                     counter: int = 0,
                     **kwargs):
        '''
            ### validates the database is fetched
            - raises `YRE.DatabaseNotFetched`
        '''
        if counter > 3:
            raise YRE.DatabaseNotFetched
        if self.db is None:
            if counter > 0:
                time.sleep(1)
            if not self.db:
                self.db = self._fetch_db()
                self.backup_db = CJson.copy_obj(self.db)
            self._validate_db(counter=counter+1)

    def _fetch_db(self,
                  **kwargs):
        '''### fetches the database'''
        return CJson.loads(self.db_path)

    def save_database(self,
                      **kwargs):
        '''
            ## saves the database
            - raises `YRE.DatabaseNotFetched`, `YRE.SaveDatabaseFailed`
        '''
        self._validate_db(counter=0)
        if self.backup_db != self.db:  # changes made
            self.backup_db = CJson.copy_obj(self.db)
            try:
                CJson.dumps(self.db, self.db_path)
            except:
                raise YRE.SaveDatabaseFailed

    def save_database_no_fail(self,
                              **kwargs):
        '''## save the database without raising any error'''
        try:
            self.save_database(**kwargs)
        except:
            pass

    def backup_database(self):
        '''## returns a backup of `self.db`'''
        self._validate_db()
        return CJson.copy_obj(self.db)

    def reset_database(self,
                       backup_database: list | dict):
        '''
            ## resets database
            ### data won't be checked
        '''
        self.db = CJson.copy_obj(backup_database)


class UserDataHandler(DatabaseHandler):
    '''
    ## Handles user database.
    - `db` must be the json format of the database
    - save the database after every change to the database
    '''

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.db_path = CONFIG.DATA_FILE_PATH

    # user

    def _validate_plan(self,
                       plan: str):
        '''
            ## validates the plan is correct
            - returns the plan if succeeds
            - raiese `YRE.PlanDoesntExist` if fails
        '''
        if plan not in CONFIG.PLANS.keys():
            raise YRE.PlanDoesntExist(plan)
        return plan

    def _validate_language(self,
                           language: str):
        '''
            ## validates the language is correct
            - returns the language if succeeds
            - raises `YRE.WrongLanguage` if fails
        '''
        return Translator.validate_language(language=language)

    def user_exists(self,
                    user_id: int | str,
                    **kwargs):
        '''
            ## returns if the user exists in the database
            - raises `YRE.DatabaseNotFetched`
        '''
        self._validate_db()
        return user_id in self.db['users'].keys()

    def create_user(self,
                    user_id: str | int,
                    user_plan: str | int,
                    user_language: str | int,
                    user_artists: List[str]):
        '''
            ## creates the user no matter what
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`,
                     `YRE.WrongLanguage` if fails
        '''
        self._validate_db()
        self.db['users'][str(user_id)] = {
            'artists': user_artists,
            'vip': self._validate_plan(plan=user_plan),
            'language': self._validate_language(language=user_language),
        }

    def _validate_user(self,
                       user_id: str | int,
                       **kwargs):
        '''
            ## creates user if not exists
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`,
                     `YRE.WrongLanguage`
        '''
        self._validate_db(counter=0)
        user_id = str(user_id)
        if user_id not in self.db['users']:
            self.create_user(user_id=user_id, user_plan=None,
                             user_language='en', user_artists=[])
        return user_id

    def user_data(self,
                  user_id: str | int,
                  **kwargs):
        '''
            ## returns data of user
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`, `YRE.WrongLanguage`
        '''
        return self.db['users'][self._validate_user(user_id=str(user_id))]

    # artists

    def artists_data(self) -> dict:
        '''
            ## returns the data of artists
            - raises `YRE.DatabaseNotFetched`
        '''
        self._validate_db()
        return self.db['artists']

    # user artist

    def add_artists(self,
                    user_id: str | int,
                    artist_ids: List[str],
                    **kwargs):
        '''
            ## Adds artists to user\n
            - returns an iterator -> `artist_index`, `artist_perform_method`\n
            - in each iteration, perform adding using `artist_perform_method` method\n
            - `perform` returns the object dictionary of the artist
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`,
                     `YRE.WrongLanguage`, `UserPlanWouldExceed` when initializing\n
            - raises `YRE.CouldntGetArtist`, `YRE.ArtistAlreadyAdded` when iterating\n

            #### Example:\n
            >>> dbh = DatabaseHandler()
            >>> artists_iter = dbh.add_artists(user_id, [artist_id])  # catch this
            >>> for artist_index, artist_perform_method in artists_iter:
                    artist = artist_perform_method() # catch this
        '''
        user_data = self.user_data(self._validate_user(user_id))
        user_artists: list = user_data['artists']
        user_plan_size = CONFIG.PLANS[user_data['vip']]['size']
        if len(user_artists) > user_plan_size:
            raise YRE.UserPlanExceeded(
                len(user_plan_size) - user_plan_size)

        if len(user_artists) + len(artist_ids) > user_plan_size:
            raise YRE.UserPlanWouldExceed(
                (len(user_artists) + len(artist_ids)) - user_plan_size)

        class AddArtistsIter(ArtistPerformIterator):
            def perform(self):
                super().perform()

                time.sleep(CONFIG.SLEEP_TIME)
                artist_id = self.artist_ids[self.index]
                artist = SpotifyHandler.get_artist(artist_id=artist_id)
                if not artist:
                    raise YRE.CouldntGetArtist(artist_id)
                artist_id, artist_name = artist['id'], artist['name']

                if artist_id in self.user_artists:
                    raise YRE.ArtistAlreadyAdded(artist_id)
                else:
                    self.user_artists.append(artist_id)
                    if artist_id not in self.db['artists'].keys():
                        albums = SpotifyHandler.get_albums(
                            artist_id=artist_id, show_first=1, artist_name=artist_name)['albums']
                        self.db['artists'][artist_id] = {
                            'urls': albums[0]['urls'],
                            'name': artist_name
                        } if len(albums) else {}
                    return artist

        return AddArtistsIter(self.db, user_id, artist_ids, user_artists)

    def del_artists(self,
                    user_id: str | int,
                    artist_ids: List[str],
                    **kwargs):
        '''
            ## Deletes artists from user\n
            - returns an iterator -> `artist_index`, `artist_perform_method`\n
            - in each iteration, perform adding using `artist_perform_method` method\n
            - `perform` returns the object dictionary of the artist
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`,
                     `YRE.WrongLanguage`, `UserPlanWouldExceed` when initializing\n
            - raises `YRE.CouldntGetArtist`, `YRE.ArtistNotAdded` when iterating\n

            #### Example:\n
            >>> dbh = DatabaseHandler()
            >>> artists_iter = dbh.del_artists(user_id, [artist_id])  # catch this
            >>> for artist_index, artist_perform_method in artists_iter:
                    artist = artist_perform_method() # catch this
        '''
        user_data = self.user_data(self._validate_user(user_id))
        user_artists: list = user_data['artists']

        class RemoveArtistsIterator(ArtistPerformIterator):
            def perform(self):
                super().perform()

                time.sleep(CONFIG.SLEEP_TIME)
                artist_id = self.artist_ids[self.index]
                artist = SpotifyHandler.get_artist(artist_id=artist_id)
                if not artist:
                    raise YRE.CouldntGetArtist(artist_id)
                artist_id, artist_name = artist['id'], artist['name']

                if artist_id not in self.user_artists:
                    raise YRE.ArtistNotAdded(artist_id)
                else:
                    self.user_artists.remove(artist_id)
                    return artist_id, artist_name

        return RemoveArtistsIterator(self.db, user_id, artist_ids, user_artists)

    # user plan

    def get_plan(self,
                 user_id: str | int,
                 **kwargs):
        '''
            ## gets the plan of the user\n
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`, `YRE.WrongLanguage`

            #### Example:
            >>> dbh = DatabaseHandler()
            >>> plan = dbh.get_plan(user_id) # catch this
        '''
        return self.user_data(self._validate_user(user_id))['vip']

    def get_plan_size(self,
                      user_id: str | int,
                      **kwargs):
        '''
            ## gets the size of the plan of the user\n
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`, `YRE.WrongLanguage`

            #### Example:
            >>> dbh = DatabaseHandler()
            >>> plan = dbh.get_plan_size(user_id) # catch this
        '''
        return CONFIG.PLANS[self.get_plan(user_id=str(user_id), **kwargs)]['size']

    def set_plan(self,
                 user_id: str | int,
                 new_plan: str,
                 **kwargs):
        '''
            ## sets the plan of the user\n
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`, `YRE.WrongLanguage`

            #### Example:
            >>> dbh = DatabaseHandler()
            >>> plan = dbh.set_plan(user_id) # catch this
        '''
        self.user_data(self._validate_user(
            user_id))['vip'] = self._validate_plan(plan=new_plan)

    # user language

    def get_language(self,
                     user_id: str | int,
                     **kwargs):
        '''
            ## gets the language of the user\n
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`, `YRE.WrongLanguage`

            #### Example:
            >>> dbh = DatabaseHandler()
            >>> plan = dbh.get_language(user_id) # catch this
        '''
        return self.user_data(self._validate_user(user_id))['language']

    def set_language(self,
                     user_id: str | int,
                     new_language: str,
                     **kwargs):
        '''
            ## sets the language of the user\n
            - raises `YRE.DatabaseNotFetched`, `YRE.PlanDoesntExist`,
                    `YRE.WrongLanguage`, `YRE.LanguageNotDetected`

            #### Example:
            >>> dbh = DatabaseHandler()
            >>> plan = dbh.set_language(user_id) # catch this
        '''
        self.user_data(
            self._validate_user(user_id)
        )['language'] = Translator.validate_language(language=new_language)


class StartedsHandler(DatabaseHandler):
    '''
        ## Handle started users
        - for the users that started this bot
        - `db` is a list
        - save the database after every change to the database
    '''

    def __init__(self,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.db_path = CONFIG.STARTEDS_FILE_APTH

    def _validate_user_id(self,
                          user_id: str | int,
                          **kwargs):
        '''### returns `user_id` as string'''
        return str(user_id)

    def add_user(self,
                 user_id: str | int,
                 **kwargs):
        '''
            ## adds user to the database if not added
            - raises `YRE.DatabaseNotFetched`
        '''
        self._validate_db()
        if (user_id := self._validate_user_id(user_id=str(user_id))) not in self.db:
            self.db.append(user_id)

    def remove_user(self,
                    user_id: str | int,
                    **kwargs):
        '''
            ## removes user from the database if added
            - raises `YRE.DatabaseNotFetched`
        '''
        self._validate_db()
        if (user_id := self._validate_user_id(user_id=str(user_id))) in self.db:
            self.db.remove(user_id)
