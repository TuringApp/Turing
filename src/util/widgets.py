# -*- coding: utf-8 -*-

import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QMessageBox


class QClickableLabel(QLabel):
    clicked = pyqtSignal()
    dclicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.last_click = None

    def mousePressEvent(self, ev):
        self.clicked.emit()
        if self.last_click and (datetime.datetime.now() - self.last_click).total_seconds() < 0.300:
            self.dclicked.emit()
        self.last_click = datetime.datetime.now()


class QFlatButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlat(True)

    def event(self, ev: QEvent):
        if ev.type() == QEvent.HoverEnter:
            self.setFlat(False)

        if ev.type() == QEvent.HoverLeave:
            self.setFlat(True)

        return super().event(ev)


def center_widget(wgt: QWidget, host: QWidget):
    if not host:
        host = wgt.parent()

    if host:
        wgt.move(host.geometry().center() - wgt.rect().center())
    else:
        wgt.move(QApplication.desktop().screenGeometry().center() - wgt.rect().center())


def get_themed_box(parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Turing")
    msg.setWindowIcon(QIcon(":/icon/media/icon.ico"))

    if parent:
        center_widget(msg, parent)

    return msg


def msg_box(text, title=None, icon=None, parent=None, buttons=QMessageBox.Yes | QMessageBox.No, default=QMessageBox.No,
            type=QMessageBox.Question):
    res = get_themed_box(parent)

    if title is not None:
        res.setWindowTitle(title)

    if icon is not None:
        res.setWindowIcon(icon)

    res.setIcon(type)
    res.setStandardButtons(buttons)
    res.setDefaultButton(default)
    res.setText(text)
    res.adjustSize()

    if parent:
        center_widget(res, parent)

    return res


def msg_box_error(text, *args, **kwargs):
    return msg_box(text, *args, **kwargs, buttons=QMessageBox.Ok, default=QMessageBox.Ok, type=QMessageBox.Critical)


def set_font_size(wgt, size, index=None):
    font = wgt.font() if index is None else wgt.font(index)
    result = QFont(font.family(), size)
    if index is None:
        wgt.setFont(result)
    else:
        wgt.setFont(index, result)
