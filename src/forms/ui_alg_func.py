# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_func.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoFuncStmt(object):
    def setupUi(self, AlgoFuncStmt):
        AlgoFuncStmt.setObjectName("AlgoFuncStmt")
        AlgoFuncStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoFuncStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoFuncStmt.setWindowIcon(icon)
        AlgoFuncStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoFuncStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoFuncStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(AlgoFuncStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.txtFunction = QtWidgets.QLineEdit(AlgoFuncStmt)
        self.txtFunction.setObjectName("txtFunction")
        self.gridLayout.addWidget(self.txtFunction, 0, 1, 1, 1)
        self.txtArguments = QtWidgets.QLineEdit(AlgoFuncStmt)
        self.txtArguments.setObjectName("txtArguments")
        self.gridLayout.addWidget(self.txtArguments, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AlgoFuncStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoFuncStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.txtFunction)
        self.label_3.setBuddy(self.txtArguments)

        self.retranslateUi(AlgoFuncStmt)
        self.buttonBox.accepted.connect(AlgoFuncStmt.accept)
        self.buttonBox.rejected.connect(AlgoFuncStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoFuncStmt)

    def retranslateUi(self, AlgoFuncStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoFuncStmt.setWindowTitle(_translate("AlgoFuncStmt", "Define function"))
        self.label.setText(_translate("AlgoFuncStmt", "<html><head/><body><p>Creates a custom function. The parameters must be a comma-separated list of identifiers.</p><p>A function may or may not return a value, it can very well only &quot;do&quot; things without ever giving a result. Such a function can be called using the CALL statement.</p></body></html>"))
        self.label_2.setText(_translate("AlgoFuncStmt", "Function:"))
        self.label_3.setText(_translate("AlgoFuncStmt", "Parameters:"))

import turing_rc
