# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_define import Ui_AlgoDefineStmt
from maths.nodes import *
from maths.parser import quick_parse as parse
from util.code import try_parse
from util.widgets import center_widget, get_themed_box

translate = QCoreApplication.translate


class AlgoDefineStmt(QDialog):
    def __init__(self, parent, origcode=("", "")):
        super().__init__(parent)
        self.ui = Ui_AlgoDefineStmt()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.ui.txtVariable.setText(origcode[0])
        self.ui.txtValue.setText(origcode[1])
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)

    def done(self, res):
        if res == QDialog.Accepted:
            name = self.ui.txtVariable.text().strip()
            parsed = parse(name)

            if not isinstance(parsed, (IdentifierNode, ArrayAccessNode)):
                box = get_themed_box(self)
                box.setIcon(QMessageBox.Critical)
                box.setStandardButtons(QMessageBox.Ok)
                box.setText(translate("Algo",
                                      "Invalid assignment target (must be either variable or array item): {name}").format(
                    name=name))
                box.adjustSize()
                center_widget(box, self)
                box.exec_()
                return

            p = try_parse(self.ui.txtValue.text(), self)

            if p is None:
                return

            self.varname = parsed
            self.expr = p
            self.ok = True

        super(AlgoDefineStmt, self).done(res)

    def click(self):
        dlg = InlineCodeDialog(self, self.ui.txtValue.text())
        if dlg.run():
            self.ui.txtValue.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
