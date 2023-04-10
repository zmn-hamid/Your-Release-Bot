'''
    # Initial values for testing
'''

import os
import logging
import unittest

from uuid import uuid4

import config as CONFIG

from Scripts.Global.YR_Exceptions import YRE

from Scripts.Global.Translator import Translator
from Scripts.Global.SpotifyHandler import SpotifyHandler
from Scripts.Global.DatabaseHandler import (
    DatabaseHandler,
    UserDataHandler,
    StartedsHandler,
)
from Scripts.Global.JSON_Handler import CJson

logging.getLogger('spotipy').setLevel(
    logging.CRITICAL)  # to silent spotipy more


class YourReleaseTestCase(unittest.TestCase):
    '''
        ## Test caes base
        - inherit this class and override `self.db_is_user_data` and
            `self.Handler`, then use `self.dbh` whenever needed
    '''

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.dbh: DatabaseHandler = None

        self.db_is_user_data: bool = None  # overrid this
        self.Handler: DatabaseHandler = None  # overrid this

    def setUp(self):
        '''Set up the test database and resources'''
        if self.db_is_user_data is None:
            raise Exception('not specified self.db_is_user_data')
        self.tests_folder = 'Tests/Temp/'
        self.test_pre_path = 'testfile-'
        self.test_db_path = self.tests_folder + \
            self.test_pre_path + str(uuid4()) + '.json'
        CJson.dumps(
            {'users': {}, 'artists': {}} if self.db_is_user_data
            else [],  # starteds db
            self.test_db_path
        )
        if self.Handler:
            self.dbh = self.Handler()
            self.dbh.db_path = self.test_db_path

    def tearDown(self):
        '''Clean up any resources used by the test'''
        for f in os.listdir(self.tests_folder):
            file_relative_path = self.tests_folder + f
            if os.path.isfile(file_relative_path) and f.startswith(self.test_pre_path):
                os.remove(file_relative_path)
