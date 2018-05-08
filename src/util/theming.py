# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import translate as translate_wrapper

app = QApplication


def translate(ctx, str):
    return lambda: translate_wrapper(ctx, str)


themes = {
    "default": (translate("Themes", "Default"),
                ["#efefef", "#000000", "#bebebe", "#ffffff", "#f7f7f7", "#ffffdc", "#000000", "#000000", "#bebebe",
                 "#9f9f9f", "#767676", "#efefef", "#000000", "#bebebe", "#ffffff", "#0000ff", "#308cc6", "#919191",
                 "#ffffff", "#ffffff", "darkred", "darkgreen", "blue", "#cb4b16"]),
    "dark": (translate("Themes", "Dark"),
             ["#353535", "#ffffff", "#7f7f7f", "#2a2a2a", "#424242", "#ffffff", "#353535", "#ffffff", "#7f7f7f",
              "#232323", "#141414", "#353535", "#ffffff", "#7f7f7f", "#ff0000", "#2a82da", "#2a82da", "#505050",
              "#ffffff", "#7f7f7f", "#ff5864", "#969696", "#45c0ef", "#fd861e"]),
    "darkblue": (translate("Themes", "Dark blue"),
                 ['#43505d', '#ebebeb', '#b0bec5', '#78909c', '#607d8b', '#ffffdc', '#ebebeb', '#ebebeb', '#bebebe',
                  '#b0bec5', '#263238', '#4e5d6c', '#ebebeb', '#b0bec5', '#eceff1', '#df691a', '#308cc6', '#607d8b',
                  '#ffffff', '#ffffff', "#eb932f", "#7cfc00", "#00ecec", "#ff7da6"]),
    "darkgreen": (translate("Themes", "Dark green"),
                  ["#435d4d", "#ebebeb", "#b0c5b6", "#789c81", "#608c69", "#ffffdc", "#ebebeb", "#ebebeb", "#bebebe",
                   "#b0c5b6", "#263826", "#546c4e", "#ebebeb", "#b0c5b6", "#edf1ec", "#df691a", "#308cc6", "#607d8b",
                   "#ffffff", "#ffffff", "#bad086", "#f2fee7", "#7cf000", "#00ef0f"]),
    "darkred": (translate("Themes", "Dark red"),
                ["#50453a", "#ebebeb", "#c5b0b0", "#8a7366", "#7a6154", "#ffffdc", "#ebebeb", "#ebebeb", "#bebebe",
                 "#c5b0b0", "#382626", "#6c4e4e", "#ebebeb", "#c5b0b0", "#f1ecec", "#df691a", "#308cc6", "#607d8b",
                 "#ffffff", "#ffffff", "#eb932f", "#7cfc00", "#00ecec", "#ff7da6"]),
    "candy": (translate("Themes", "Candy"),
              ["#f51278", "#161059", "#cacaca", "#ff49a1", "#ff77be", "#ffffff", "#000000", "#000732", "#c62528",
               "#48002d", "#000000", "#ff20c4", "#000732", "#71292a", "#00ffd9", "#5500ff", "#000732", "#0003d9",
               "#17e1d4", "#0a645e", "#ad00bd", "#aa003b", "#a30fff", "#277008"]),
    "devtest": (lambda: "DEVTEST", []),
    "custom": (translate("Themes", "Custom"), [])
}

default_algo_colors = themes["default"][1][20:]
algo_colors = default_algo_colors


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
    global algo_colors
    algo_colors = default_algo_colors


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
        global algo_colors
        algo_colors = clr[20:24]

    app.setStyleSheet("QLineEdit { padding: 3px }")
