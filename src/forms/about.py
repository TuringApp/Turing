# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.ui_about import Ui_AboutWindow
from util.widgets import center_widget

translate = QCoreApplication.translate


def init_ui(parent, version, channel):
    global window, ui
    window = QDialog()
    ui = Ui_AboutWindow()
    ui.setupUi(window)
    window.setFixedSize(window.size())
    txt = ui.textBrowser_about.toHtml().replace("{version}", version).replace("{channel}", channel)
    ui.textBrowser_about.setHtml(txt)
    center_widget(window, parent)
    window.exec_()



def run(parent, version, channel):
    init_ui(parent, version, channel)
