# -*- coding: utf-8 -*-

import html
import re

from PyQt5.QtGui import *

import maths.lib.docs
import translator
from maths.evaluator import Evaluator
from ui_calculator import Ui_CalcWindow
from util.math import proper_str
from widgets import *

translate = QCoreApplication.translate

functions = None
doc_items = None


def find_func(name):
    for k in functions:
        for f in functions[k]:
            if f[0] == name:
                return k, f

    return None


def add_result(expr, result, error=False):
    if expr:
        item1 = QListWidgetItem()

        txt = str(expr)
        item1.setText(txt)
        item1.setStatusTip(txt)

        ui.lstHistory.addItem(item1)

    item2 = QListWidgetItem()

    txt = proper_str(result)
    item2.setText(txt)

    item2.setTextAlignment(Qt.AlignRight)

    if error:
        item2.setForeground(QBrush(QColor("red")))
    else:
        item2.setStatusTip(txt)

    ui.lstHistory.addItem(item2)

    ui.lstHistory.scrollToBottom()


def calculate():
    ev = Evaluator()
    expression = ui.txtExpr.text()

    result = ev.evaluate(expression)
    msgs = ev.log.get_messages()

    if msgs:
        err = "\n".join([x[1] for x in msgs])
        add_result(ev.beautified, err, True)

    if result is not None:
        add_result(None if msgs else ev.beautified, result)
    else:
        add_result(None if msgs else ev.beautified, translate("CalcWindow", "Result is None"), True)


def history_double_click(item):
    if item.statusTip():
        ui.txtExpr.setText(item.text())


def on_sel(id):
    for idx, items in enumerate(doc_items):
        for it in items:
            it.setHidden(idx != id)


def load_funcs():
    global functions, doc_items
    functions = maths.lib.get_funcs()
    doc_items = []
    for k in sorted(functions.keys()):
        ui.cbxFuncs.addItem(k)
        doc_items.append([])

        for f in sorted(functions[k], key=lambda x: x[0]):
            item_func = QListWidgetItem(ui.listWidget)
            w = QWidget()
            lay = QVBoxLayout()

            label_func = QLabel()
            label_func.setText(maths.lib.docs.get_func_def_html(f))

            lay.addWidget(label_func)

            label_desc = QLabel()
            desc = re.sub(r"{{(\w+)\}\}", "<i><b>\g<1></b></i>", html.escape(f[2]))
            desc = re.sub(r"//(\w+)//", "<i>\g<1></i>", desc)

            label_desc.setText(desc)

            label_desc.setAlignment(Qt.AlignRight)

            lay.addWidget(label_desc)
            lay.setSizeConstraint(QLayout.SetFixedSize)
            lay.setSpacing(2)
            lay.setContentsMargins(6, 6, 6, 6)
            w.setLayout(lay)
            item_func.setSizeHint(w.sizeHint())
            ui.listWidget.setItemWidget(item_func, w)
            doc_items[-1].append(item_func)
            item_func.setStatusTip(f[0])


def ins_func(item):
    ui.txtExpr.setText(ui.txtExpr.text() + item.statusTip() + "()")


def clear():
    ui.txtExpr.setText("")


def txt_changed(txt):
    ui.btnClear.setVisible(bool(txt))


def init_ui():
    global window, ui
    window = QMainWindow()
    ui = Ui_CalcWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    ui.btnCalc.clicked.connect(calculate)
    ui.lstHistory.itemDoubleClicked.connect(history_double_click)
    ui.listWidget.itemDoubleClicked.connect(ins_func)

    load_funcs()

    ui.cbxFuncs.currentIndexChanged.connect(on_sel)
    ui.txtExpr.textChanged.connect(txt_changed)
    ui.btnClear.clicked.connect(clear)
    ui.btnClear.setVisible(False)

    on_sel(0)

    window.show()


def run():
    init_ui()
