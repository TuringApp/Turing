# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_if import Ui_AlgoIfStmt
from util.code import try_parse
from util.widgets import center_widget

translate = QCoreApplication.translate


class AlgoIfStmt(QDialog):
    def __init__(self, parent, origcode=""):
        super().__init__(parent)
        self.ui = Ui_AlgoIfStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.lineEdit.setText(origcode)
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)

    def done(self, res):
        if res == QDialog.Accepted:
            p = try_parse(self.ui.lineEdit.text(), self)

            if p is None:
                return

            self.expr = p
            self.ok = True

        super(AlgoIfStmt, self).done(res)

    def click(self):
        dlg = InlineCodeDialog(self, self.ui.lineEdit.text())
        self.ui.lineEdit.setText(dlg.run())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
