# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_call import Ui_AlgoCallStmt
from maths.nodes import ListNode
from util.code import try_parse
from util.widgets import center_widget

translate = QCoreApplication.translate


class AlgoCallStmt(QDialog):
    def __init__(self, parent, origcode=("", ())):
        super().__init__(parent)
        self.ui = Ui_AlgoCallStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.txtFunction.setText(origcode[0])
        self.ui.txtArguments.setText(", ".join(origcode[1]))
        self.ui.btnCodeFunc.clicked.connect(lambda: self.click(self.ui.txtFunction))
        self.ui.btnCodeArgs.clicked.connect(lambda: self.click(self.ui.txtArguments))
        center_widget(self, parent)

    def done(self, res):
        if res == QDialog.Accepted:
            p = try_parse(self.ui.txtFunction.text(), self)

            if p is None:
                return

            self.func = p

            p = try_parse("[%s]" % self.ui.txtArguments.text(), self)

            if p is None or not isinstance(p, ListNode):
                return

            self.args = p.value

            self.ok = True

        super(AlgoCallStmt, self).done(res)

    def click(self, wgt):
        dlg = InlineCodeDialog(self, wgt.text())
        if dlg.run():
            wgt.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
