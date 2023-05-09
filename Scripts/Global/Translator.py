'''
    # Translate text
'''

from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as LANGS

from Scripts.Global.YR_Exceptions import YRE


class BaseTranslator:
    '''
        ## Google Translator
        - translate any language to the desired language
        - set language using `set_language`
    '''

    def __init__(self, base_language: str = 'en') -> None:
        self.language = None
        self.base_language = Translator.validate_language(
            language=base_language)

    @staticmethod
    def validate_language(language: str):
        '''
            ## validates the language is correct
            - raises `YRE.LanguageNotDetected`
            - returns language if no fail
        '''
        if language not in list(LANGS.keys()) + list(LANGS.values()):
            raise YRE.WrongLanguage('language not detected')
        return language

    def get_language(self):
        '''## get the current language'''
        return self.language

    def set_language(self, language: str):
        '''## set the language'''
        self.language = Translator.validate_language(language=language)

    def do(self, text: str) -> str:
        '''
            ## do the translation
            - raises `YRE.NoLanguageSet`
        '''
        if not self.language:
            raise YRE.NoLanguageSet
        if self.base_language == self.language:
            return text
        return GoogleTranslator(source=self.base_language,
                                target=self.language).translate(text)


class Translator(BaseTranslator):
    '''
        ## does nothing
        the previous translator faced a lot of problems when translating html codings.
        So i removed this function completely. But to make it take less time,
        and also to keep the original translator code, I inherited it and turned off everything
    '''

    def __init__(self, base_language: str = 'en') -> None:
        pass

    @staticmethod
    def validate_language(language: str):
        return 'en'

    def get_language(self):
        return 'en'

    def set_language(self, language: str):
        pass

    def do(self, text: str) -> str:
        return text
