# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime

class QClickableLabel(QLabel):
    clicked = pyqtSignal()
    dclicked = pyqtSignal()
    last_click = None

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()
        if self.last_click and (datetime.datetime.now() - self.last_click).total_seconds() < 0.300:
            self.dclicked.emit()
        self.last_click = datetime.datetime.now()