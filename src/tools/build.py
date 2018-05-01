#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from PyQt5.QtCore import QLibraryInfo

subprocess.call([
    "pyinstaller",
    "--onefile",
    "--additional-hooks-dir=.",
    "--icon=media/icon.ico",
    "--hidden-import",
    "colorsys",
    "--windowed",
    "--add-data",
    os.pathsep.join([QLibraryInfo.location(QLibraryInfo.TranslationsPath), "PyQt5/Qt/translations"]),
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
