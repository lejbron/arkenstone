
## Используемые файлы конфигураций

- VSCode:
	+ `launch.json` - профили запуска проекта для пошаговой отладки.
	+ `settings.json` - локальный файл настроек vscode.
- [.editorconfoig](https://editorconfig.org/) - настройки плагинов, проверяющих соблюдение единого стиля кода. Для работы с VSCode необходимо установить [соответсвующий плагин](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).
- `.pre-commit-config.yaml` - список хуков, используемых в проекте.
- [Procfile](https://devcenter.heroku.com/articles/procfile) - файл с командами, которые выполняются на серверах Heroku при заупске приложения.
- [runtime.txt](https://devcenter.heroku.com/articles/python-runtimes) - файл, в котором фиксируется используемая для запуска приложения на серверах Heroku версия python.
- `setup.cfg` - настройки python-пакетов.
