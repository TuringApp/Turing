# -*- coding: utf-8 -*-

from PyQt5.QtGui import *

from forms.inline_code_editor import InlineCodeEditor
from forms.ui_calculator import Ui_CalcWindow
from lang import translator
from maths.evaluator import Evaluator
from util.math import proper_str
from util.widgets import *

translate = QCoreApplication.translate


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CalcWindow()

        translator.add(self.ui, self)
        self.ui.setupUi(self)

        self.editor = InlineCodeEditor(self.ui.centralwidget)
        self.ui.verticalLayout.addWidget(self.editor)
        self.editor.submitted.connect(self.calculate)

        self.ui.lstHistory.itemDoubleClicked.connect(self.history_double_click)

        self.show()

    def add_result(self, expr, result, error=False):
        if expr:
            item1 = QListWidgetItem()

            txt = str(expr)
            item1.setText(txt)
            item1.setStatusTip(txt)

            self.ui.lstHistory.addItem(item1)

        item2 = QListWidgetItem()

        txt = proper_str(result)
        item2.setText(txt)

        item2.setTextAlignment(Qt.AlignRight)

        if error:
            item2.setForeground(QBrush(QColor("red")))
        else:
            item2.setStatusTip(txt)

        self.ui.lstHistory.addItem(item2)

        self.ui.lstHistory.scrollToBottom()

    def calculate(self):
        ev = Evaluator()
        expression = self.editor.get_text()

        result = ev.evaluate(expression)
        msgs = ev.log.get_messages()

        if msgs:
            # err = "\n".join([x[1] for x in msgs])
            err = msgs[0][1]
            self.add_result(ev.beautified, err, True)
        else:
            if result is not None:
                self.add_result(None if msgs else ev.beautified, result)
            else:
                self.add_result(None if msgs else ev.beautified, translate("CalcWindow", "Result is None"), True)

    def history_double_click(self, item):
        if item.statusTip():
            self.editor.set_text(item.text())
