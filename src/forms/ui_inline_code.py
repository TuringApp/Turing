# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_inline_code.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InlineCodeDialog(object):
    def setupUi(self, InlineCodeDialog):
        InlineCodeDialog.setObjectName("InlineCodeDialog")
        InlineCodeDialog.setWindowModality(QtCore.Qt.WindowModal)
        InlineCodeDialog.resize(453, 241)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        InlineCodeDialog.setWindowIcon(icon)
        InlineCodeDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(InlineCodeDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(InlineCodeDialog)
        QtCore.QMetaObject.connectSlotsByName(InlineCodeDialog)

    def retranslateUi(self, InlineCodeDialog):
        _translate = QtCore.QCoreApplication.translate
        InlineCodeDialog.setWindowTitle(_translate("InlineCodeDialog", "Expression editor"))

import turing_rc
