# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.ui_display_stmt import Ui_DisplayWindow
from util.widgets import center_widget

global dialog_window
translate = QCoreApplication.translate

def new_display():
    new_display = ui.lineInput.text()
    return new_display


def init_ui(parent, version, channel):
    global window, ui
    window = QDialog()
    ui = Ui_DisplayWindow()
    ui.setupUi(window)
    window.setFixedSize(window.size())
    center_widget(window, parent)
    
    ui.buttonBox.clicked.connect(new_display)
    
    window.exec_()

def run(parent, version, channel):
    init_ui(parent, version, channel)