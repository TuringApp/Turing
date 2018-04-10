#!/bin/bash

pyinstaller --onefile --additional-hooks-dir=. --icon=media/icon.ico --windowed -n turing -y main.py
pyinstaller --onefile --additional-hooks-dir=. --icon=media/icon.ico --hidden-import pyqode.python.backend -y editor_backend.py

