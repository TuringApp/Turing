#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QLibraryInfo
import subprocess

subprocess.call([
    "pyinstaller",
    "--onefile",
    "--additional-hooks-dir=.",
    "--icon=media/icon.ico",
    "--hidden-import",
    "colorsys",
    "--windowed",
    "--add-data",
    r'%s;PyQt5\Qt\translations' % QLibraryInfo.location(QLibraryInfo.TranslationsPath),
    "-n",
    "turing",
    "-y",
    "main.py"
])

subprocess.call([
    "pyinstaller",
    "--onefile",
    "--additional-hooks-dir=.",
    "--icon=media/icon.ico",
    "--hidden-import",
    "pyqode.python.backend",
    "-y",
    "editor_backend.py"
])