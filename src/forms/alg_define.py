# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_define import Ui_AlgoDefineStmt
from util.widgets import center_widget, get_themed_box
from util.code import try_parse, is_id

translate = QCoreApplication.translate

class AlgoDefineStmt(QDialog):
    def __init__(self, parent, origcode=("", "")):
        super().__init__(parent)
        self.ui = Ui_AlgoDefineStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.txtVariable.setText(origcode[0])
        self.ui.txtValue.setText(origcode[1])
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)


    def done(self, res):
        if res == QDialog.Accepted:
            name = self.ui.txtVariable.text().strip()
            if not is_id(name):
                box = get_themed_box(self)
                box.setIcon(QMessageBox.Critical)
                box.setStandardButtons(QMessageBox.Ok)
                box.setText(translate("Algo", "Invalid variable name: {name}").format(name=name))
                box.exec_()
                return

            p = try_parse(self.ui.txtValue.text(), self)

            if p is None:
                return

            self.varname = name
            self.expr = p

        super(AlgoDefineStmt, self).done(res)


    def click(self):
        dlg = InlineCodeDialog(self, self.ui.txtValue.text())
        if dlg.run():
            self.ui.txtValue.setText(dlg.value())


    def run(self):
        return self.exec_() == QDialog.Accepted and self.expr is not None
