# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_display import Ui_AlgoDisplayStmt
from util.code import try_parse
from util.widgets import center_widget

translate = QCoreApplication.translate


class AlgoDisplayStmt(QDialog):
    def __init__(self, parent, origcode=("", True)):
        super().__init__(parent)
        self.ui = Ui_AlgoDisplayStmt()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.ui.lineEdit.setText(origcode[0])
        self.ui.cbxNewline.setChecked(origcode[1])
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)

    def done(self, res):
        if res == QDialog.Accepted:
            p = try_parse(self.ui.lineEdit.text(), self)

            if p is None:
                return

            self.expr = p
            self.newline = self.ui.cbxNewline.isChecked()
            self.ok = True

        super(AlgoDisplayStmt, self).done(res)

    def click(self):
        dlg = InlineCodeDialog(self, self.ui.lineEdit.text())
        if dlg.run():
            self.ui.lineEdit.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
