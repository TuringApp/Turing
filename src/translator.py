# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
import os

uis = []
current = "en"

def add(u, w):
    uis.append((u, w))

def remove(u):
    global uis
    uis = [x for x in uis if x[0] != u]

def update():
    for u, w in uis:
        u.retranslateUi(w)

def translate(c, t):
    if current != "en":
        a = QTranslator()
        a.load(current, "lang")
        QCoreApplication.installTranslator(a)
    return QCoreApplication.translate2(c, t)


def load(lang):
    global current
    current = lang
    update()