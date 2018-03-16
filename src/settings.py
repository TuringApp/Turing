# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_settings import Ui_SettingsWindow

translate = QCoreApplication.translate


def init_ui():
    global window, ui
    window = QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(window)
    window.show()


def run():
    init_ui()
