'''
    # Testing database handler
'''

from Tests import *


class ResetDatabaseHandlerTestCase(YourReleaseTestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db_is_user_data = True
        self.Handler = UserDataHandler
        self.dbh: UserDataHandler

    def test_reset_database_succeeds(self):
        user_id, artist_id = 'test-user', '01xUafSGlkbklhhimae66R'
        add_artists_iter = self.dbh.add_artists(user_id, [artist_id])
        for artist_idx, artist_perform in add_artists_iter:
            artist_perform()
            self.assertIn(artist_id, self.dbh.db['users'][user_id]['artists'])
        self.dbh.save_database()
        self.assertTrue(len(self.dbh.db['users'][user_id]['artists']) == 1)

        # reset
        self.dbh.reset_database(backup_database=[])
        self.dbh.save_database()
        self.dbh.db = {'users': {}, 'artists': {}}
