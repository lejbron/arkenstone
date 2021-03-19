# Arkenstone Onboarding Guide

Перед началом работы над проектом внимательно ознакомьтесь с [Arkenstone Codestyle](https://github.com/lejbron/arkenstone/blob/master/docs/arc_codestyle.md).

## Настройка окружения

- [.pre-commit-config.yaml](https://pre-commit.com/#2-add-a-pre-commit-configuration) - список хуков, используемых в проекте.
- [.editorconfoig](https://editorconfig.org/) - настройки плагинов, проверяющих соблюдение единого стиля кода.
- `.jsbeautifyrc` - настройки стиля html-шаблонов для плагина `Beautify`.
- [Procfile](https://devcenter.heroku.com/articles/procfile) - файл с командами, которые выполняются на серверах Heroku при заупске приложения.
- [runtime.txt](https://devcenter.heroku.com/articles/python-runtimes) - файл, в котором фиксируется используемая для запуска приложения на серверах Heroku версия python.
- `setup.cfg` - настройки python-пакетов.

## Настройки проекта

В проекте используется отдельные настройки для dev и prod сред:
- Общие настройки: `arkenston/settings/base.py`
- Development: `arkenston/settings/dev.py`
- Production: `arkenston/settings/prod.py`

## Настройка VSCode

### Терминал

- Для корректной работы терминала задайте в Visual Studio Code ассоциацию с `python` из установленной виртуальной среды:
	+ Windows:
		- перейдитие на вкладку `File > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/Scripts/python.exe`.
	+ Linux and macOS:
		- перейдитие на вкладку `Code > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/bin/python`.

### Плагины

- [Editorconfig](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- [Beautify](https://marketplace.visualstudio.com/items?itemName=HookyQR.beautify)

### Пример settings.json

```
{
    "python.pythonPath": ".venv/bin/python",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "editor.rulers": [119],
    "debug.inlineValues": true,
    "files.insertFinalNewline": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true,
        },
    },
    "[html]": {
        "editor.defaultFormatter": "HookyQR.beautify",
        "editor.formatOnSave": true,
    }
}
```
