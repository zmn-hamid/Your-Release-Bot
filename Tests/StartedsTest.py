'''
    # Testing starteds database handler
'''

from Tests import *


class StartedsHandlerTestCase(YourReleaseTestCase):
    '''
        ## Test case for starteds
    '''

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db_is_user_data = False
        self.Handler = StartedsHandler
        self.dbh: StartedsHandler  # for pylance

    def test_add_user_succeeds(self):
        user_id = 'test-user'
        self.dbh.add_user(user_id=user_id)
        self.assertIn(user_id, self.dbh.backup_database())

    def test_remove_user_succeeds(self):
        user_id = 'test-user'
        self.dbh.add_user(user_id=user_id)
        self.assertIn(user_id, self.dbh.backup_database())

        self.dbh.remove_user(user_id=user_id)
        self.assertNotIn(user_id, self.dbh.backup_database())
