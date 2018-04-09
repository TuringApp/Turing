# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.inline_code_dialog import InlineCodeDialog
from forms.ui_alg_gwindow import Ui_AlgoGWindowStmt
from util.code import try_parse, is_id
from util.widgets import center_widget, get_themed_box

translate = QCoreApplication.translate


class AlgoGWindowStmt(QDialog):
    def __init__(self, parent, origcode=("", "", "", "", "", "")):
        super().__init__(parent)
        self.ui = Ui_AlgoGWindowStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.txtXmin.setText(origcode[0])
        self.ui.txtXmax.setText(origcode[1])
        self.ui.txtYmin.setText(origcode[2])
        self.ui.txtYmax.setText(origcode[3])
        self.ui.txtXgrad.setText(origcode[2])
        self.ui.txtYgrad.setText(origcode[3])

        self.ui.btnCodeXmin.clicked.connect(lambda: self.click(self.ui.txtXmin))
        self.ui.btnCodeXmax.clicked.connect(lambda: self.click(self.ui.txtXmax))
        self.ui.btnCodeYmin.clicked.connect(lambda: self.click(self.ui.txtYmin))
        self.ui.btnCodeYmax.clicked.connect(lambda: self.click(self.ui.txtYmax))
        self.ui.btnCodeXgrad.clicked.connect(lambda: self.click(self.ui.txtXgrad))
        self.ui.btnCodeYgrad.clicked.connect(lambda: self.click(self.ui.txtYgrad))

        center_widget(self, parent)


    def done(self, res):
        if res == QDialog.Accepted:
            p = try_parse(self.ui.txtXmin.text(), self)

            if p is None:
                return

            self.f_x_min = p

            p = try_parse(self.ui.txtXmax.text(), self)

            if p is None:
                return

            self.f_x_max = p

            p = try_parse(self.ui.txtYmin.text(), self)

            if p is None:
                return

            self.f_y_min = p

            p = try_parse(self.ui.txtYmax.text(), self)

            if p is None:
                return

            self.f_y_max = p

            p = try_parse(self.ui.txtXgrad.text(), self)

            if p is None:
                return

            self.f_x_grad = p

            p = try_parse(self.ui.txtYgrad.text(), self)

            if p is None:
                return

            self.f_y_grad = p

            self.ok = True

        super(AlgoGWindowStmt, self).done(res)

    def click(self, wgt):
        dlg = InlineCodeDialog(self, wgt.text())
        if dlg.run():
            wgt.setText(dlg.value())

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
