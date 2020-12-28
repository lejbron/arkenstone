# Arkenstone Onboarding Guide

Для начала работы над проектом выполните следующие действия:

- Склонируйте репозиторий `arkenstone` с [GitHub](https://github.com/lejbron/arkenstone).
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

- Внимтально ознакомьтесь с Arkenstone codestyle.