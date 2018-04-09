# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_gpoint import Ui_AlgoGPointStmt
from util.code import try_parse, is_id
from util.widgets import center_widget, get_themed_box

translate = QCoreApplication.translate


class AlgoGPointStmt(QDialog):
    def __init__(self, parent, origcode=("", "", '"red"')):
        super().__init__(parent)
        self.ui = Ui_AlgoGPointStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.txtX.setText(origcode[0])
        self.ui.txtY.setText(origcode[1])
        self.ui.txtColor.setText(origcode[2])

        self.ui.btnCodeX.clicked.connect(lambda: self.click(self.ui.txtX))
        self.ui.btnCodeY.clicked.connect(lambda: self.click(self.ui.txtY))
        self.ui.btnCodeColor.clicked.connect(lambda: self.click(self.ui.txtColor))

        center_widget(self, parent)


    def done(self, res):
        if res == QDialog.Accepted:
            p = try_parse(self.ui.txtX.text(), self)

            if p is None:
                return

            self.f_x = p

            p = try_parse(self.ui.txtY.text(), self)

            if p is None:
                return

            self.f_y = p

            p = try_parse(self.ui.txtColor.text(), self)

            if p is None:
                return

            self.f_color = p

            self.ok = True

        super(AlgoGPointStmt, self).done(res)

    def click(self, wgt):
        dlg = InlineCodeDialog(self, wgt.text())
        if dlg.run():
            wgt.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
