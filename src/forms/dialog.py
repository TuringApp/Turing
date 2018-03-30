# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.ui_addDisplay import Ui_AddDisplayWindow
from util.widgets import center_widget

translate = QCoreApplication.translate


def init_ui(parent, version, channel):
    global window, ui
    window = QDialog()
    ui = Ui_AddDisplayWindow()
    ui.setupUi(window)
    window.setFixedSize(window.size())
    center_widget(window, parent)
    window.exec_()


def run(parent, version, channel):
    init_ui(parent, version, channel)
