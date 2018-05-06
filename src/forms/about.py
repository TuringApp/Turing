# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication, QMovie
from PyQt5.QtWidgets import *

from forms.ui_about import Ui_AboutWindow
from util.widgets import center_widget

translate = QCoreApplication.translate


class AboutWindow(QDialog):
    KONAMI = [Qt.Key_Up, Qt.Key_Up, Qt.Key_Down, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, Qt.Key_Left, Qt.Key_Right, Qt.Key_B, Qt.Key_A]

    def __init__(self, parent, version, channel):
        super().__init__(parent)
        self.kpos = 0
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        txt = self.ui.textBrowser_about.toHtml().replace("{version}", version).replace("{channel}", channel)
        self.ui.textBrowser_about.setHtml(txt)
        QGuiApplication.instance().installEventFilter(self)
        center_widget(self, parent)

    def closeEvent(self, QCloseEvent):
        QGuiApplication.instance().removeEventFilter(self)

    def keyPressEvent(self, QKeyEvent):
        if AboutWindow.KONAMI[self.kpos] == QKeyEvent.key():
            self.kpos += 1
            if self.kpos >= len(AboutWindow.KONAMI):
                self.egg()
        else:
            self.kpos = 0

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True

        return False

    def egg(self):
        self.kpos = 0
        movie = QMovie(":/action/media/media.qrc")
        self.ui.label.setText(None)
        self.ui.label.setMovie(movie)
        movie.start()
        self.setStyleSheet("QDialog { background-color: red; }")

    def run(self):
        self.exec_()
