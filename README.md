# localize-py
```
>>> _ = Translator('eng')
>>> _('about', why='Because it's simple')
'Localization module that requires no more than JSON files of fields.
- Why is it good?
- Because it's simple'
```
# Installation
```
pip install localize-py
```
# Be Aware
This module abuses f-strings, thus there are several requirements:
- \>=Python 3.6
- Extreme awareness of user input - I personally wouldn't add user input to variables, unless I've checked it.
- Some symbols require escaping in JSON, e.g.:
    - \n -> \\\n
    - { -> {{
    - \ -> \\\
    - And similar

You will see examples of escaping below.
# HowTo
-- How do I create them?

-- JSON files with dictionary for each language, not more, not less. 
```
# /eng_file.json
{
    "Button1": "Return",
    "Button2": "Hello, {username}"
}
# /esp_file.json
{
    "Button1": "Volver",
    "Button2": "Hola, {username}"
}
```
-- How do I use them?

-- Well, not much harder than create. Let's consider an imaginary web application:
```
from localize_py import Translator
def app_start():
    Translator.load_translations(eng='/eng_file.json', esp='/esp_file.json')

def handle_client_request(request):
    lang = get_client_lang_from_database(request)
    _ = Translator(lang)
    return _('Button1'), _('Button2', username=request.client.name)
```
Here are two **nonsense** functions - `app_start` and `handle_client_request`. 
It's better to load translation files on start of application, that's why it's `app_start`.
`load_translation` is a static function does exactly what you expect from its name. You can pass it shortnames for languages from your DB as argument names and paths to files as values.
When you need to translate text finally, simply initialize an instance of `Translator` with correct shortname, and then even simplier - call it as a function and provide a tag (key) for target string.

-- Now what does that `{username}` thing mean?

-- You can subsitute variables from your code to the translation by passing them as key arguments to `__call__`, right after string tag.
```
# /eng_file.json
{ "Button1": "Hello, {username}" }

# program.py
from localize_py import Translator
Translator.load_translations(eng='/eng_file.json')
_ = Translator('eng')
_('Button1', username='Alex')

# Output: "Hello, Alex"
```

# Additional utility for Russian language plural forms
In order to make correct plural forms in Russian one could use `ru_plural` function inside of translation:
```
/rus_file.json
{
  "some_plural": "Доступно {amount} {['акция', 'акции', 'акций'][self.ru_plural(amount)]}:\\n"
}

# program.py
from localize_py import Translator
Translator.load_translations(eng='/rus_file.json')
_ = Translator('rus')
_('some_plural', amount=25)

# Output: "Доступно 25 акций"
```

Normal API documentation will appear soon, however, it's already presented in sources, so your IDE will show it.
