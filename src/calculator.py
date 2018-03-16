# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_calculator import Ui_CalcWindow
from maths.parser import Parser
from maths.evaluator import Evaluator
from util.math import properstr
import maths.lib.docs
import re

fns = None
items = []


def find_func(name):
    for k in fns:
        for f in fns[k]:
            if f[0] == name:
                return (k, f)
    return None


def addResult(expr, result, error=False):
    if expr:
        i1 = QListWidgetItem()
        txt = str(expr)
        i1.setText(txt)
        i1.setToolTip(txt)
        ui.lstHistory.addItem(i1)

    i2 = QListWidgetItem()
    txt = properstr(result)
    i2.setText(txt)
    i2.setTextAlignment(Qt.AlignRight)
    if error:
        i2.setForeground(QBrush(QColor("red")))
    else:
        i2.setToolTip(txt)
    ui.lstHistory.addItem(i2)
    ui.lstHistory.scrollToBottom()


def calc():
    ev = Evaluator()
    expr = ui.txtExpr.text()
    ret = ev.evaluate(expr)
    msgs = ev.log.getMessages()
    if msgs:
        err = "\n".join([x[1] for x in msgs])
        addResult(ev.beautified, err, True)
    if ret is not None:
        addResult(None if msgs else ev.beautified, ret)
    else:
        addResult(None if msgs else ev.beautified, "Result is None", True)


def dclick(item):
    if item.toolTip():
        ui.txtExpr.setText(item.text())


def on_sel(id):
    for i in range(len(items)):
        for it in items[i]:
            it.setHidden(i != id)


def load_funcs():
    global fns
    fns = maths.lib.get_funcs()
    for k in sorted(fns.keys()):
        ui.cbxFuncs.addItem(k)
        items.append([])
        for f in sorted(fns[k], key=lambda x: x[0]):
            i = QListWidgetItem()
            fnt = i.font()
            fnt.setBold(True)
            i.setFont(fnt)
            i.setText(maths.lib.docs.get_func_def(f))
            i.setWhatsThis(f[0])

            items[-1].append(i)
            ui.listWidget.addItem(i)

            d = QListWidgetItem()
            desc = re.sub(r"{{(\w+)\}\}", "\g<1>", f[2])
            desc = re.sub(r"//(\w+)//", "\g<1>", desc)
            d.setText(desc)
            d.setTextAlignment(Qt.AlignRight)
            d.setWhatsThis(f[0])

            items[-1].append(d)
            ui.listWidget.addItem(d)


def ins_func(item):
    ui.txtExpr.setText(ui.txtExpr.text() + item.whatsThis() + "()")


def clear():
    ui.txtExpr.setText("")


def txt_changed(txt):
    ui.btnClear.setVisible(bool(txt))


def initUi():
    global window, ui
    window = QMainWindow()
    ui = Ui_CalcWindow()
    ui.setupUi(window)
    ui.btnCalc.clicked.connect(calc)
    ui.lstHistory.itemDoubleClicked.connect(dclick)
    ui.listWidget.itemDoubleClicked.connect(ins_func)
    load_funcs()
    ui.cbxFuncs.currentIndexChanged.connect(on_sel)
    ui.txtExpr.textChanged.connect(txt_changed)
    ui.btnClear.clicked.connect(clear)
    ui.btnClear.setVisible(False)
    on_sel(0)
    window.show()


def run():
    initUi()
