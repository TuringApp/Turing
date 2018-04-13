# -*- coding: utf-8 -*-

import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QMessageBox


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


def get_themed_box(parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Turing")
    msg.setWindowIcon(QIcon(":/icon/media/icon.ico"))

    if parent:
        center_widget(msg, parent)

    return msg


def set_font_size(wgt, size, index=None):
    font = wgt.font() if index is None else wgt.font(index)
    result = QFont(font.family(), size)
    if index is None:
        wgt.setFont(result)
    else:
        wgt.setFont(index, result)