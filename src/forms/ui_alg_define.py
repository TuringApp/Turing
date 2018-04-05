# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_define.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoDefineStmt(object):
    def setupUi(self, AlgoDefineStmt):
        AlgoDefineStmt.setObjectName("AlgoDefineStmt")
        AlgoDefineStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoDefineStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoDefineStmt.setWindowIcon(icon)
        AlgoDefineStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoDefineStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoDefineStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(AlgoDefineStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoDefineStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.txtVariable = QtWidgets.QLineEdit(AlgoDefineStmt)
        self.txtVariable.setObjectName("txtVariable")
        self.gridLayout.addWidget(self.txtVariable, 0, 1, 1, 1)
        self.txtValue = QtWidgets.QLineEdit(AlgoDefineStmt)
        self.txtValue.setObjectName("txtValue")
        self.gridLayout.addWidget(self.txtValue, 1, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoDefineStmt)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoDefineStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AlgoDefineStmt)
        self.buttonBox.accepted.connect(AlgoDefineStmt.accept)
        self.buttonBox.rejected.connect(AlgoDefineStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoDefineStmt)

    def retranslateUi(self, AlgoDefineStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoDefineStmt.setWindowTitle(_translate("AlgoDefineStmt", "Define variable"))
        self.label.setText(_translate("AlgoDefineStmt", "<html><head/><body><p>Assigns the specified value to the variable.</p><p>If the variable does not exist in the current scope or in any parent scope, it will be created in the current scope.</p></body></html>"))
        self.label_3.setText(_translate("AlgoDefineStmt", "Value:"))
        self.label_2.setText(_translate("AlgoDefineStmt", "Variable:"))

import turing_rc
