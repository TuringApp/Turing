# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_input import Ui_AlgoInputStmt
from maths.nodes import *
from maths.parser import quick_parse as parse
from util.code import try_parse
from util.widgets import center_widget, msg_box_error

translate = QCoreApplication.translate


class AlgoInputStmt(QDialog):
    def __init__(self, parent, origcode=("", None, False)):
        super().__init__(parent)
        self.ui = Ui_AlgoInputStmt()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.ui.txtVariable.setText(origcode[0])
        self.ui.cbxHasValue.stateChanged.connect(self.checked)
        self.ui.cbxHasValue.setChecked(origcode[1] is not None)
        if origcode[1] is not None:
            self.ui.txtValue.setText(origcode[1])
        self.ui.cbxText.setChecked(origcode[2])
        self.ui.btnCode.clicked.connect(self.click)
        center_widget(self, parent)

    def checked(self, state):
        enabled = state == Qt.Checked
        self.ui.txtValue.setEnabled(enabled)
        self.ui.btnCode.setEnabled(enabled)

    def done(self, res):
        if res == QDialog.Accepted:
            name = self.ui.txtVariable.text().strip()
            parsed = parse(name)

            if not isinstance(parsed, (IdentifierNode, ArrayAccessNode)):
                box = msg_box_error(translate("Algo",
                                              "Invalid assignment target (must be either variable or array item): {name}").format(
                    name=name), parent=self)
                box.exec_()
                return

            if self.ui.cbxHasValue.isChecked():
                p = try_parse(self.ui.txtValue.text(), self)

                if p is None:
                    return

                self.expr = p
            else:
                self.expr = None

            self.text = self.ui.cbxText.isChecked()
            self.varname = parsed
            self.ok = True

        super(AlgoInputStmt, self).done(res)

    def click(self):
        dlg = InlineCodeDialog(self, self.ui.txtValue.text())
        if dlg.run():
            self.ui.txtValue.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
