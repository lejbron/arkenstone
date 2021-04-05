[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![GitHub license](https://img.shields.io/github/license/lejbron/arkenstone)](https://github.com/lejbron/arkenstone/blob/master/LICENSE)
[![Discord](https://img.shields.io/discord/487183213618397185?label=arkenstone&logo=discord&style=social)](https://discord.gg/RBkPNJYhjw)


# Arkenstone

Добро пожаловать на страницу проекта Arkenstone - сайта для организации турниров по настольным варгеймам!

Пользователи сайта смогут:
- зарегистрироваться на сайте
- регистрироваться на актуальные турниры
- в реальном времени следить за проходящим турниром
- отслеживать прогресс формирования рейтинга
- обсуждать с другими игроками все события, связанные с турниром

Организаторы турниров будут иметь возможность:
- управлять ходом турнира
- обрабатывать заявки на регистрацию
- вносить результаты матчей

## Установка

- Склонируйте репозиторий [arkenstone](https://github.com/lejbron/arkenstone).
- В корневой папке проекта создайте виртуальную среду python:
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
- Установите необходимые зависимости с помощью `pip`:
```
pip install -r requirements.txt
```
- Установите pre-commit hook для вашего репозитория, выполнив в корневой папке проекта команду:
```
pre-commit install
```

> В данном проекте ветка master используется **ТОЛЬКО** для текущей рабочей версии сайта. `pre-commit` hook запрещает делать commit в ветку master и является обязательным для установки.
Также он берет на себя проверку соблюдения PEP8 и сортирует импорты с помощью isort, упрощая codereview.

- Установите [PostgreSQL](https://www.postgresql.org/download/) для вашей операционной системы и создайте базу данных в pgadmin (нажать правой кнопкой мыши на `Databases` и выбрать пункт `Create`).
- Скопируйте файл `.env.template`, переименуйте его в `.env` и задайте в нем все значения переменных.

## Зависимости проекта

Backend сайта написан на django, в процессе разработки соблюдается [единый стиль кода](https://github.com/lejbron/arkenstone/blob/master/docs/arc_codestyle.md).

Все необходимые зависимости перечислены в [requirements.txt](https://github.com/lejbron/arkenstone/blob/master/requirements.txt).

При определении текущей версии приложения используется подход [семантического версионирования](https://semver.org/lang/ru/). Номер версии - MAJOR.MINOR.PATCH.

## Запуск проекта

По умолчанию выполнение команды `python manage.py runserver` запустит сервер с использованием настроек dev-среды.
При необходимости использовать другой файл настроек, измените значение переменной `DJANGO_SETTINGS_MODULE` в файле `manage.py`.

## Участникам проекта

Настройка окружения для работы над проектом описана в [инструкции](https://github.com/lejbron/arkenstone/blob/master/docs/get_on_board.md).

В процессе работы необходимо соблюдать [правила наименования веток](https://github.com/lejbron/arkenstone/blob/master/docs/branch_policy.md).

## Документация

- [Карта сайта](https://drive.google.com/file/d/1L9HJCxISj05P-uX8s6-EZ4jgd87GMYG8/view?usp=sharing)
- [ERD](https://drive.google.com/file/d/1eyMkw809fLA8hwQQFUq9-8wouB04VEzy/view?usp=sharing)
- [Status-flow проведения турнира](https://drive.google.com/file/d/1ztib1LcFU_Z4qif4fevw-4glTEQ_UR85/view?usp=sharing)
- [Пользовательские сценарии](https://docs.google.com/spreadsheets/d/1-0XJSyblXo-fqIp7M5ilByEk8yUb91jx0wxa1dGEdLY/edit?usp=sharing)
- [Общие принципы разработки](https://github.com/lejbron/arkenstone/blob/master/docs/best_practices.md)
- [Структура проекта](https://github.com/lejbron/arkenstone/blob/master/docs/arc_structure.md)

## Текущая версия

Текущаяю версия сайта работает на [басплатном тарифе](https://www.heroku.com/pricing) хостинга Heroku.
Ограничения:
- 600 часов работы сервера в месяц.
- 10000 записей в базе данных - [Postgres Heroku add-on](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier).
- Сервер засыпает через 30 мин при отсутствии активности.
