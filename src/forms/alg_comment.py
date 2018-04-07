# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from forms.ui_alg_comment import Ui_AlgoCommentStmt
from util.widgets import center_widget

translate = QCoreApplication.translate


class AlgoCommentStmt(QDialog):
    def __init__(self, parent, origcode=""):
        super().__init__(parent)
        self.ui = Ui_AlgoCommentStmt()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.lineEdit.setText(origcode)
        center_widget(self, parent)

    def done(self, res):
        if res == QDialog.Accepted:
            self.comment = self.ui.lineEdit.text()
            self.ok = True

        super(AlgoCommentStmt, self).done(res)

    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
