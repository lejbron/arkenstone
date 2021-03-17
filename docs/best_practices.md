# Separated settings

- Вместо файла `settings.py` создается папка `settings` с пустым файлом `__init_.py`.
- Настройки разбиваются на файлы:
    + общие найстройки для всех сред
    + настройки среды разработки
    + настройки боевого сервера
- Файл с общими настройками подключается в начале файлов настроек сред:
    ```
    from .base import *  # noqa
    ```

Для запуска сервера django с определенными настройками можно:
- непосредсвенно указывать используемый файл при выполнении команды запуска сервера:
    ```
    python manage.py runserver --settings=mysite.settings.dev
    python manage.py migrate --settings=mysite.settings.prod
    ```
- задать значение `DJANGO_SETTINGS_MODULE` непосредственно в файле запуска - `manage.py`:
    ```
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
    ```

Подробное описание разделенеия `settings.py` на несколько файлов приводится в [статье](https://simpleisbetterthancomplex.com/tips/2017/07/03/django-tip-20-working-with-multiple-settings-modules.html)

# Separated views

- Вместо файла `views.py` создается папка `views`.
- В папке создается файл `__init__.py`, в котором импортируются все view-функции, содержащиеся в файлах внутри папки.
- Создается необходимое количество `views_name.py` файлов.

При созаднии новых view-функций **не забывайте** добавлять их в import в файле `__init__.py`!

Подробное описание разделенеия `views.py` на несколько файлов привеодится в [статье](https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html).

# Signals

Все операции, реагирующие на сигналы Django, хранятся в файлах `signals.py`. Для подключения файла к приложению выполните следующие действия:

    - В файле `apps.py` добавьте код:
        ```
        from django.apps import AppConfig

        class MyAppConfig(AppConfig):
            name = 'app_name'
            def ready(self):
                import app_name.signals  # noqa
        ```
    - В файле `__init__.py` приложения задайте значение:
        ```
        default_app_config = 'app_name.apps.AppNameConfig'
        ```