import json
from functools import lru_cache


class Translator():
    '''
    Simple module for localization

    Example of usage in imaginary web application:
    On application load:
        Translator.load_translations(eng='path/to/file.json')

    On client connection:
        lang = get_client_language_from_db() # returns 'eng'
        _ = Translator(lang)
        return _('TextBox1', username=client.name)

    Keep in mind that this module uses lru_cache in order to provide faster translations of complex strings
    '''

    def __init__(self, language=None):
        '''Initialize client text translator with given language'''
        self.language = language

    def __del__(self):
        '''
        Simple destructor - explicitly clears cache
        '''
        self.__call__.cache_clear()
        self.__getitem__.cache_clear()
        self.__delattr__('language')

    @lru_cache(typed=True)
    def __call__(self, tag, **kwargs):
        '''
        Function that returns translated to the client's language text by provided tag
        Additionally, it substitutes variables that meets in text

        Arguments:
        tag: required, name of dictionary key from JSON translation file
        **Key arguments - values of variables from translation strings

        Example:
        if __name__ == '__main__':
            Translator.load_translations(eng='/file/example.json')
        ...
        _ = Translator('eng')
        return _('TextBox1', username='Alex')
        '''
        string = getattr(Translator, self.language)[tag]
        if not kwargs:
            kwargs = dict()
        return eval(''.join([f'f\"', string, '\"']), {'self': self}, kwargs)

    @lru_cache(typed=True)
    def __getitem__(self, tag, **kwargs):
        '''
        Basically the same __call__
        '''
        return self(tag, **kwargs)

    def backwards(self, text):
        '''
        The function tries to translate user input to the variable
        (Get button name from label, for instance)

        Keep in mind, won't work with variables in strings
        '''
        lang = getattr(self, f'inverse_{self.language}')
        return lang[text]

    @staticmethod
    def ru_plural(x):
        '''
        For Russian language only.
        Function that helps to choose word ending in Russian.

        endings = ['акция', 'акции', 'акций']
        print(endings[Translator.ru_plural(25)])
        >> 'акций'

        Can be used in translations files:
        {
          "Button1": "Назад",
          "Button2": "Старт",
          "TextBox1": "Добро пожаловать, {username}!\\n",
          "RuPlural": "доступно {amount} {['акция', 'акции', 'акций'][self.ru_plural(amount)]}:\\n"
        }
        '''
        lastTwoDigits = x % 100
        tens = lastTwoDigits / 10
        if tens == 1:
            return 2
        ones = lastTwoDigits % 10
        if ones == 1:
            return 0
        if ones >= 2 and ones <= 4:
            return 1
        return 2

    @staticmethod
    def load_translations(**translations):
        '''
        Load JSON files of translations and label them with language shortcuts
        File example:
        {
          "Button1": "Return",
          "Button2": "Start",
          "TextBox1": "Welcome, {username}!"
        }
        Usage example:
        if __name__ == '__main__':
            Translator.load_translations(eng='/file/example.json')
        '''
        for language, file in translations.items():
            with open(file, 'r') as file:
                data = json.load(file)
                setattr(Translator, language, data)
                setattr(Translator, f'inverse_{language}', dict([(v, k) for k, v in getattr(Translator, language).items()]))

    def unload_translations(*translations):
        '''
        Unload translations from provided list.
        Does not affect existing instances, unless cached
        '''
        for language in translations:
            delattr(Translator, language)
            delattr(Translator, f'inverse_{language}')
