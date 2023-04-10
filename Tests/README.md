## Tests folder

Steps to use this folder (for developers):

1. Create a test file here
2. `from Tests import *`
3. Create a test method and inherit it from `YourReleaseTestCase`
4. Initialize it, use `super` to initialize the parent, then set these variables:
   ```
   self.db_is_user_data = True  # if the main database is the users db (True) or starteds db (False)
   self.Handler = UserDataHandler  # the database handler (all of them are imported in the parent file)
   self.dbh: UserDataHandler  # [optional] for pylance
   ```
5. Import everything from this file to [tests.py](../tests.py)
6. In the main directory, run `python tests.py`
