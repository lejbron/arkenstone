
## Используемые файлы конфигураций

- VSCode:
	+ `launch.json` -
	+ `settings.json` -
- `.editorconfoig` -
- `.pre-commit-config.yaml` -
- `Procfile` -
- `runtime.txt` -
- `setup.cfg` -




- Установите в Visual Studio Code ассоциацию с `python` из установленной виртуальной среды:
	+ Windows:
		- перейдитие на вкладку `File > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/Scripts/python.exe`.
	+ Linux and macOS:
		- перейдитие на вкладку `Code > Preferences > Settings`;
		- найдите константу `python.pythonPath`;
		- задайте ей значение `./.venv/bin/python`.