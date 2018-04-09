@echo off
pyinstaller --onefile --additional-hooks-dir=. --icon=media/icon.ico -y main.py
pyinstaller --onefile --additional-hooks-dir=. --icon=media/icon.ico -y editor_backend.py