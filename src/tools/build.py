#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from PyQt5.QtCore import QLibraryInfo

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

subprocess.call([
    "pyinstaller",
    "--onefile",
    "--additional-hooks-dir=.",
    "--icon=media/icon." + ("icns" if sys.platform == "darwin" else "ico"),
    "--hidden-import",
    "colorsys",
    "--windowed",
    "--add-data",
    os.pathsep.join([QLibraryInfo.location(QLibraryInfo.TranslationsPath), "PyQt5/Qt/translations"]),
    "--add-data",
    os.pathsep.join([os.path.join("dist", "editor_backend" + (".exe" if sys.platform == "win32" else "")), "/"]),
    "-n",
    "turing",
    "-y",
    "main.py"
])
