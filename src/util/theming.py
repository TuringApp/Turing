# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from util import translate


app = QApplication

themes = {
    "default": (lambda: translate("Themes", "Default"), []),
    "dark": (lambda: translate("Themes", "Dark"), ["#353535", "#ffffff", "#7f7f7f", "#2a2a2a", "#424242", "#ffffff", "#353535", "#ffffff", "#7f7f7f", "#232323", "#141414", "#353535", "#ffffff", "#7f7f7f", "#ff0000", "#2a82da", "#2a82da", "#505050", "#ffffff", "#7f7f7f"]),
    "darkblue": (lambda: translate("Themes", "Dark blue"), ['#43505d', '#ebebeb', '#b0bec5', '#78909c', '#607d8b', '#ffffdc', '#ebebeb', '#ebebeb', '#bebebe', '#b0bec5', '#263238', '#4e5d6c', '#ebebeb', '#b0bec5', '#eceff1', '#df691a', '#308cc6', '#607d8b', '#ffffff', '#ffffff']),
    "devtest": (lambda: "DEVTEST", []),
    "custom": (lambda: translate("Themes", "Custom"), [])
}


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


def reset_theme():
    init_theming()


def load_theme(name):
    reset_theme()

    p = app.palette()

    if name in themes and themes[name][1]:
        clr = themes[name][1]
        p.setColor(QPalette.Window, QColor(clr[0]))
        p.setColor(QPalette.WindowText, QColor(clr[1]))
        p.setColor(QPalette.Disabled, QPalette.WindowText, QColor(clr[2]))
        p.setColor(QPalette.Base, QColor(clr[3]))
        p.setColor(QPalette.AlternateBase, QColor(clr[4]))
        p.setColor(QPalette.ToolTipBase, QColor(clr[5]))
        p.setColor(QPalette.ToolTipText, QColor(clr[6]))
        p.setColor(QPalette.Text, QColor(clr[7]))
        p.setColor(QPalette.Disabled, QPalette.Text, QColor(clr[8]))
        p.setColor(QPalette.Dark, QColor(clr[9]))
        p.setColor(QPalette.Shadow, QColor(clr[10]))
        p.setColor(QPalette.Button, QColor(clr[11]))
        p.setColor(QPalette.ButtonText, QColor(clr[12]))
        p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(clr[13]))
        p.setColor(QPalette.BrightText, QColor(clr[14]))
        p.setColor(QPalette.Link, QColor(clr[15]))
        p.setColor(QPalette.Highlight, QColor(clr[16]))
        p.setColor(QPalette.Disabled, QPalette.Highlight, QColor(clr[17]))
        p.setColor(QPalette.HighlightedText, QColor(clr[18]))
        p.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(clr[19]))
        app.setPalette(p)

    app.setStyleSheet("QLineEdit { padding: 3px }")