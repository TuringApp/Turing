# -*- coding: utf-8 -*-

import html
import re
from typing import Dict, List, Tuple

from PyQt5.QtGui import *

import maths.lib.docs
from forms.ui_calculator import Ui_CalcWindow
from lang import translator
from maths.evaluator import Evaluator
from util.math import proper_str
from util.widgets import *
from forms.inline_code_editor import InlineCodeEditor

translate = QCoreApplication.translate


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
    expression = editor.get_text()

    result = ev.evaluate(expression)
    msgs = ev.log.get_messages()

    if msgs:
        # err = "\n".join([x[1] for x in msgs])
        err = msgs[0][1]
        add_result(ev.beautified, err, True)
    else:
        if result is not None:
            add_result(None if msgs else ev.beautified, result)
        else:
            add_result(None if msgs else ev.beautified, translate("CalcWindow", "Result is None"), True)


def history_double_click(item):
    if item.statusTip():
        editor.set_text(item.text())


def init_ui():
    global window, ui, editor
    window = QMainWindow()
    ui = Ui_CalcWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    editor = InlineCodeEditor(ui.centralwidget)
    ui.verticalLayout.addWidget(editor)
    editor.submitted.connect(calculate)


    ui.lstHistory.itemDoubleClicked.connect(history_double_click)


    window.show()


def run():
    init_ui()
