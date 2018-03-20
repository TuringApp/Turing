# -*- coding: utf-8 -*-

import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


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


def center_widget(wgt: QWidget, host: QWidget):
    if not host:
        host = wgt.parent()

    if host:
        wgt.move(host.geometry().center() - wgt.rect().center())
    else:
        wgt.move(QCoreApplication.desktop().screenGeometry().center() - wgt.rect().center())
