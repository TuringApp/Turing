# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from util import translate


app = QApplication


def init_theming():
    if "Fusion" in [st for st in QStyleFactory.keys()]:
        app.setStyle(QStyleFactory.create("Fusion"))
    elif sys.platform == "win32":
        app.setStyle(QStyleFactory.create("WindowsVista"))
    elif sys.platform == "linux":
        app.setStyle(QStyleFactory.create("gtk"))
    elif sys.platform == "darwin":
        app.setStyle(QStyleFactory.create("macintosh"))

    app.setPalette(QApplication.style().standardPalette())


def set_localized_name(name):
    def decorator(func):
        func.name = name
        return func
    return decorator


@set_localized_name(translate("Themes", "Default"))
def theme_default(p):
    pass


@set_localized_name(translate("Themes", "Dark"))
def theme_dark(p):
    p.setColor(QPalette.Window, QColor(53, 53, 53))
    p.setColor(QPalette.WindowText, Qt.white)
    p.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    p.setColor(QPalette.Base, QColor(42, 42, 42))
    p.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    p.setColor(QPalette.ToolTipBase, Qt.white)
    p.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
    p.setColor(QPalette.Text, Qt.white)
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    p.setColor(QPalette.Dark, QColor(35, 35, 35))
    p.setColor(QPalette.Shadow, QColor(20, 20, 20))
    p.setColor(QPalette.Button, QColor(53, 53, 53))
    p.setColor(QPalette.ButtonText, Qt.white)
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    p.setColor(QPalette.BrightText, Qt.red)
    p.setColor(QPalette.Link, QColor(42, 130, 218))
    p.setColor(QPalette.Highlight, QColor(42, 130, 218))
    p.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
    p.setColor(QPalette.HighlightedText, Qt.white)
    p.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))


def get_themes():
    return {n[6:]: f for n, f in globals().items() if n.startswith("theme_")}


def reset_theme():
    init_theming()


def load_theme(name):
    reset_theme()

    p = app.palette()

    if name in get_themes() and not globals()["theme_" + name](p):
        app.setPalette(p)
    else:
        reset_theme()

    app.setStyleSheet("QLineEdit { padding: 3px }")