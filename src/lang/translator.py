# -*- coding: utf-8 -*-

import importlib
import sip
import types
from typing import List, Tuple

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

uis: List[Tuple[object, QWidget]] = []
current_lang = None
tr_object: QTranslator = None
tr_object_qt: QTranslator = None


def add(ui: object, window: QWidget):
    uis.append((ui, window))


def remove(ui: object):
    global uis
    uis = [x for x in uis if x[0] != ui]


def update():
    import maths.lib
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
    global current_lang, tr_object, tr_object_qt
    current_lang = lang
    locale = QLocale(lang)
    if tr_object:
        QCoreApplication.removeTranslator(tr_object)
        QCoreApplication.removeTranslator(tr_object_qt)

    tr_object = QTranslator()
    if not tr_object.load(locale, "", "", ":/lang/lang"):
        if not tr_object.load(lang, ":/lang/lang"):
            print("error loading %s" % lang)
    tr_object_qt = QTranslator()

    if not tr_object_qt.load(locale, "qt", "_", QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
        tr_object_qt.load(locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.TranslationsPath))

    QCoreApplication.installTranslator(tr_object_qt)
    QCoreApplication.installTranslator(tr_object)

    QLocale.setDefault(locale)
    update()
