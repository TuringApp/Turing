# -*- coding: utf-8 -*-

import importlib
import types

from PyQt5.QtCore import *

import maths.lib

uis = []
current = None
tr_object = None

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
        if isinstance(item, types.ModuleType) and not name.startswith("__") and name != "docs":
            importlib.reload(item)


def load(lang):
    global current, tr_object
    current = lang

    if tr_object:
        QCoreApplication.removeTranslator(tr_object)

    tr_object = QTranslator()
    tr_object.load(current, "lang")

    QCoreApplication.installTranslator(tr_object)

    QLocale.setDefault(QLocale(lang))
    update()
