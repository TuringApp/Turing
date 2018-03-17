# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
import os
import importlib
import maths.lib
import types

uis = []
current = None


def add(ui, window):
    uis.append((ui, window))


def remove(ui):
    global uis
    uis = [x for x in uis if x[0] != ui]


def update():
    for ui, window in uis:
        ui.retranslateUi(window)

    # reload the docs
    importlib.reload(maths.lib.docs)
    for name, item in maths.lib.__dict__.items():
        if type(item) == types.ModuleType and not name.startswith("__") and name != "docs":
            importlib.reload(item)


def translate(context, string):
    if current != "en_US":
        tr_object = QTranslator()
        tr_object.load(current, "lang")
        QCoreApplication.installTranslator(tr_object)

    return QCoreApplication.translate2(context, string)


def load(lang):
    global current
    current = lang
    QLocale.setDefault(QLocale(lang))
    update()
