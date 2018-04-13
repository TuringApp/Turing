# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_return import Ui_AlgoReturnStmt
from util.code import try_parse
from util.widgets import center_widget

translate = QCoreApplication.translate


class AlgoReturnStmt(QDialog):
    def __init__(self, parent, origcode=None):
        super().__init__(parent)
        self.ui = Ui_AlgoReturnStmt()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.ui.cbxHasValue.stateChanged.connect(self.checked)
        self.ui.cbxHasValue.setChecked(origcode is not None)
        if origcode is not None:
            self.ui.txtValue.setText(origcode)
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)

    def checked(self, state):
        enabled = state == Qt.Checked
        self.ui.txtValue.setEnabled(enabled)
        self.ui.btnCode.setEnabled(enabled)

    def done(self, res):
        if res == QDialog.Accepted:
            if self.ui.cbxHasValue.isChecked():
                p = try_parse(self.ui.txtValue.text(), self)

                if p is None:
                    return

                self.expr = p
            else:
                self.expr = None

            self.ok = True

        super(AlgoReturnStmt, self).done(res)

    def click(self):
        dlg = InlineCodeDialog(self, self.ui.txtValue.text())
        if dlg.run():
            self.ui.txtValue.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
