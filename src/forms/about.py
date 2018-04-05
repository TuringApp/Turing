# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.ui_about import Ui_AboutWindow
from util.widgets import center_widget

translate = QCoreApplication.translate

class AboutWindow(QDialog):
    def __init__(self, parent, version, channel):
        super().__init__(parent)
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        txt = self.ui.textBrowser_about.toHtml().replace("{version}", version).replace("{channel}", channel)
        self.ui.textBrowser_about.setHtml(txt)
        center_widget(self, parent)

    def run(self):
        self.exec_()
