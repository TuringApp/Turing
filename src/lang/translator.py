# -*- coding: utf-8 -*-

import importlib
import sip
import types
from typing import List, Tuple

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

import maths.lib

uis: List[Tuple[object, QWidget]] = []
current = None
tr_object: QTranslator = None


def add(ui: object, window: QWidget):
    uis.append((ui, window))


def remove(ui: object):
    global uis
    uis = [x for x in uis if x[0] != ui]


def update():
    global uis
    uis = [x for x in uis if not sip.isdeleted(x[1])]

    for ui, window in uis:
        ui.retranslateUi(window)

    # reload the docs
    importlib.reload(maths.lib.docs)
    for name, item in maths.lib.__dict__.items():
        if isinstance(item, types.ModuleType) and not name.startswith("__") and name != "docs":
            importlib.reload(item)


def load(lang: str):
    global current, tr_object
    current = lang

    if tr_object:
        QCoreApplication.removeTranslator(tr_object)

    tr_object = QTranslator()
    tr_object.load(current, ":/lang/lang")

    QCoreApplication.installTranslator(tr_object)

    QLocale.setDefault(QLocale(lang))
    update()
