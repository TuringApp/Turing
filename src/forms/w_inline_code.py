# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'w_inline_code.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InlineCodeEditor(object):
    def setupUi(self, InlineCodeEditor):
        InlineCodeEditor.setObjectName("InlineCodeEditor")
        InlineCodeEditor.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(InlineCodeEditor)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtExpr = QtWidgets.QLineEdit(InlineCodeEditor)
        self.txtExpr.setObjectName("txtExpr")
        self.horizontalLayout.addWidget(self.txtExpr)
        self.btnClear = QtWidgets.QPushButton(InlineCodeEditor)
        self.btnClear.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon)
        self.btnClear.setObjectName("btnClear")
        self.horizontalLayout.addWidget(self.btnClear)
        self.btnSubmit = QtWidgets.QPushButton(InlineCodeEditor)
        self.btnSubmit.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSubmit.setIcon(icon1)
        self.btnSubmit.setObjectName("btnSubmit")
        self.horizontalLayout.addWidget(self.btnSubmit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbxFuncs = QtWidgets.QComboBox(InlineCodeEditor)
        self.cbxFuncs.setObjectName("cbxFuncs")
        self.verticalLayout_2.addWidget(self.cbxFuncs)
        self.lstFuncs = QtWidgets.QListWidget(InlineCodeEditor)
        self.lstFuncs.setObjectName("lstFuncs")
        self.verticalLayout_2.addWidget(self.lstFuncs)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(InlineCodeEditor)
        QtCore.QMetaObject.connectSlotsByName(InlineCodeEditor)

    def retranslateUi(self, InlineCodeEditor):
        _translate = QtCore.QCoreApplication.translate
        InlineCodeEditor.setWindowTitle(_translate("InlineCodeEditor", "Form"))

import turing_rc
