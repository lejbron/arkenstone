# Arkenstone Onboarding Guide

Перед началом работы над проектом внимательно ознакомьтесь с [Arkenstone Codestyle](https://github.com/lejbron/arkenstone/blob/master/docs/Arcenstone_codestyle.md).

## Настройка окружения

- Склонируйте репозиторий [arkenstone](https://github.com/lejbron/arkenstone).
- Создайте виртульную среду python, выполнив в папке проекта (arkenstone) следующую команду:
```
python -m venv .venv
```
- Активируйте виртуальную среду командой:
	+ Windows:
	```
	.venv\Scripts\activate.bat
	```
	+ Linux или macOS:
	```
	source .venv/bin/activate
	```
- Установите необходимые зависимости с попощью `pip`:
```
pip install -r requirements.txt
```
- Установите pre-commit hook для вашего репозитория, выполнив в папке проекта (arkenstone) команду:
```
pre-commit install
```

- Установите в Visual Studio Code ассоциацию с `python` из установленной виртуальной среды:
	+ Windows:
		- перейдитие на вкладку `File > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/Scripts/python.exe`.
	+ Linux and macOS:
		- перейдитие на вкладку `Code > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/bin/python`.

## Настройки проекта

В проекте используется отдельные настройки для dev и prod сред.
- Общие настройки: `arkenston/settings/base.py`.
- Development: `arkenston/settings/dev.py`
- Production: `arkenston/settings/prod.py`

Текущаяю версия сайта работает на [басплатном тарифе](https://www.heroku.com/pricing) хостинга Heroku.
Ограничения:
- 600 часов работы сервера в месяц.
- 10000 записей в базе данных - [Postgres Heroku add-on](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier).
- Сервер засыпает через 30 мин при отсуствии активности.

Для локального запуска необхомо настроить переменные окружени:
- Скопируйте файл `.env.template` и переименуйте его в `.env`.
- Укажите необходимые значения, соответсвующие вашему окружению.

## Подключение базы данных
