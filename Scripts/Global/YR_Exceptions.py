class YR_Exceptions(Exception):
    ...


class YRE:
    class DatabaseNotFetched(YR_Exceptions):
        '''## possible error to fetch database'''

    class SaveDatabaseFailed(YR_Exceptions):
        '''## to handle when the database can't be saved'''

    class UserPlanExceeded(YR_Exceptions):
        '''## to catch when user '''

    class UserPlanWouldExceed(YR_Exceptions):
        '''## to catch when user '''

    class CouldntGetArtist(YR_Exceptions):
        '''## to catch when user '''

    class ArtistAlreadyAdded(YR_Exceptions):
        '''## artist already added'''

    class ArtistNotAdded(YR_Exceptions):
        '''## artist not added at all'''

    class PlanDoesntExist(YR_Exceptions):
        '''## to handle when wrong user plan chosen'''

    class WrongLanguage(YR_Exceptions):
        '''## to reject non correct languages'''

    class NoLanguageSet(YR_Exceptions):
        '''## when no language is specified'''

    class Starteds:
        class DatabaseNotFetched(YR_Exceptions):
            '''## possible error to fetch database'''
