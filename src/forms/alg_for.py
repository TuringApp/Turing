# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_for import Ui_AlgoForStmt
from util.code import try_parse, is_id
from util.widgets import center_widget, get_themed_box

translate = QCoreApplication.translate


class AlgoForStmt(QDialog):
    def __init__(self, parent, origcode=("", "", "", None)):
        super().__init__(parent)
        self.ui = Ui_AlgoForStmt()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.ui.txtVariable.setText(origcode[0])
        self.ui.txtFrom.setText(origcode[1])
        self.ui.txtTo.setText(origcode[2])

        self.ui.cbxHasValue.stateChanged.connect(self.checked)
        self.ui.cbxHasValue.setChecked(origcode[3] is not None)
        if origcode[3] is not None:
            self.ui.txtStep.setText(origcode[3])

        self.ui.btnCodeFrom.clicked.connect(lambda: self.click(self.ui.txtFrom))
        self.ui.btnCodeTo.clicked.connect(lambda: self.click(self.ui.txtTo))
        self.ui.btnCodeStep.clicked.connect(lambda: self.click(self.ui.txtStep))

        center_widget(self, parent)

    def checked(self, state):
        enabled = state == Qt.Checked
        self.ui.txtStep.setEnabled(enabled)
        self.ui.btnCodeStep.setEnabled(enabled)

    def done(self, res):
        if res == QDialog.Accepted:
            name = self.ui.txtVariable.text().strip()
            if not is_id(name):
                box = get_themed_box(self)
                box.setIcon(QMessageBox.Critical)
                box.setStandardButtons(QMessageBox.Ok)
                box.setText(translate("Algo", "Invalid variable name: {name}").format(name=name))
                box.adjustSize()
                center_widget(box, self)
                box.exec_()
                return

            p = try_parse(self.ui.txtFrom.text(), self)

            if p is None:
                return

            self.f_from = p

            p = try_parse(self.ui.txtTo.text(), self)

            if p is None:
                return

            self.f_to = p

            if self.ui.cbxHasValue.isChecked():
                p = try_parse(self.ui.txtStep.text(), self)

                if p is None:
                    return

                self.f_step = p
            else:
                self.f_step = None

            self.varname = name
            self.ok = True

        super(AlgoForStmt, self).done(res)

    def click(self, wgt):
        dlg = InlineCodeDialog(self, wgt.text())
        if dlg.run():
            wgt.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
