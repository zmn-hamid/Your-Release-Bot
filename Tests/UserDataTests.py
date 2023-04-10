'''
    # Testing user database handler
'''

from Tests import *


class UserDatabaseHandlerTestCase(YourReleaseTestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db_is_user_data = True
        self.Handler = UserDataHandler
        self.dbh: UserDataHandler


class UserDatabaseHandlerAddArtistTestCase(UserDatabaseHandlerTestCase):
    def test_add_artist_succeeds(self):
        user_id, artist_id = 'test-user', '01xUafSGlkbklhhimae66R'
        add_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in add_artists_iter:
            artist_perform()
            self.assertIn(artist_id, self.dbh.db['users'][user_id]['artists'])
        self.dbh.save_database()
        self.assertTrue(len(self.dbh.db['users'][user_id]['artists']) == 1)

    def test_add_repetitive_artist_fails(self):
        user_id, artist_id = 'test-user', '01xUafSGlkbklhhimae66R'

        CJson.dumps(self.dbh.db, 'temp/t1')
        add_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in add_artists_iter:
            artist_perform()
            self.assertIn(artist_id, self.dbh.db['users'][user_id]['artists'])
        self.dbh.save_database()

        # repeat
        add_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in add_artists_iter:
            try:
                artist_perform()
                self.assertFalse(True)
            except YRE.ArtistAlreadyAdded as e:
                ...
        self.dbh.save_database()
        self.assertTrue(len(self.dbh.db['users'][user_id]['artists']) == 1)

    def test_add_wrong_url_fails(self):
        user_id, artist_id = 'test-user', 'wrong ID/URL/URI'
        add_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in add_artists_iter:
            try:
                artist_perform()
                self.assertFalse(True)
            except YRE.CouldntGetArtist as e:
                ...
        self.dbh.save_database()
        self.assertTrue(len(self.dbh.db['users'][user_id]['artists']) == 0)


class UserDatabaseHandlerDelArtistTestCase(UserDatabaseHandlerTestCase):
    def test_del_artist_succeeds(self):
        user_id, artist_id = 'test-user', '01xUafSGlkbklhhimae66R'
        # add artist
        del_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in del_artists_iter:
            artist_perform()
            self.assertIn(artist_id, self.dbh.db['users'][user_id]['artists'])
        self.dbh.save_database()

        # remove artist
        del_artists_iter = self.dbh.del_artists(user_id, [artist_id])
        for artist_idx, artist_perform in del_artists_iter:
            artist_perform()
            self.assertNotIn(
                artist_id, self.dbh.db['users'][user_id]['artists'])
        self.dbh.save_database()
        self.assertNotIn(artist_id, self.dbh.db['users'][user_id]['artists'])

    def test_del_non_existing_artist_fails(self):
        user_id, artist_id = 'test-user', '01xUafSGlkbklhhimae66R'
        del_artists_iter = self.dbh.del_artists(user_id, [artist_id])
        for artist_idx, artist_perform in del_artists_iter:
            try:
                artist_perform()
                self.assertFalse(True)
            except YRE.ArtistNotAdded as e:
                ...
        self.dbh.save_database()
        self.assertNotIn(artist_id, self.dbh.db['users'][user_id]['artists'])

    def test_del_wrong_url_fails(self):
        user_id, artist_id = 'test-user', 'wrong ID/URL/URI'
        del_artists_iter = self.dbh.del_artists(user_id, [artist_id])
        for artist_idx, artist_perform in del_artists_iter:
            try:
                artist_perform()
                self.assertFalse(True)
            except YRE.CouldntGetArtist as e:
                ...
        self.dbh.save_database()
        self.assertNotIn(artist_id, self.dbh.db['users'][user_id]['artists'])


class UserDatabaseHandlerUserPlanTestCase(UserDatabaseHandlerTestCase):
    def test_set_plan_succeeds(self):
        user_id, user_plan = 'test-user', 'A'
        self.dbh.create_user(user_id=user_id, user_plan=user_plan,
                             user_language='en', user_artists=[])
        self.assertEquals(self.dbh.get_plan(user_id=user_id), user_plan)
        self.assertEquals(self.dbh.get_plan_size(user_id=user_id),
                          CONFIG.PLANS[user_plan]['size'])

    def test_set_wrong_plan_fails(self):
        user_id, user_plan = 'test-user', 'wrong plan'
        try:
            self.dbh.create_user(user_id=user_id, user_plan=user_plan,
                                 user_language='en', user_artists=[])
            self.assertFalse(True)
        except YRE.PlanDoesntExist as e:
            ...


class UserDatabaseHandlerUserLanguageTestCase(UserDatabaseHandlerTestCase):
    def test_set_language_succeeds(self):
        user_id, user_language = 'test-user', 'en'
        self.dbh.create_user(user_id=user_id, user_plan=None,
                             user_language=user_language, user_artists=[])
        self.assertEquals(self.dbh.get_language(
            user_id=user_id), user_language)

    def test_set_wrong_language_fails(self):
        user_id, user_language = 'test-user', 'wrong language'
        try:
            self.dbh.create_user(user_id=user_id, user_plan=None,
                                 user_language=user_language, user_artists=[])
            self.assertFalse(True)
        except YRE.WrongLanguage as e:
            ...
