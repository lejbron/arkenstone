# Separated settings

# Separated views

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