# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_call.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoCallStmt(object):
    def setupUi(self, AlgoCallStmt):
        AlgoCallStmt.setObjectName("AlgoCallStmt")
        AlgoCallStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoCallStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoCallStmt.setWindowIcon(icon)
        AlgoCallStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoCallStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoCallStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(AlgoCallStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.btnCodeFunc = QtWidgets.QPushButton(AlgoCallStmt)
        self.btnCodeFunc.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCodeFunc.setIcon(icon1)
        self.btnCodeFunc.setObjectName("btnCodeFunc")
        self.gridLayout.addWidget(self.btnCodeFunc, 0, 2, 1, 1)
        self.txtFunction = QtWidgets.QLineEdit(AlgoCallStmt)
        self.txtFunction.setObjectName("txtFunction")
        self.gridLayout.addWidget(self.txtFunction, 0, 1, 1, 1)
        self.btnCodeArgs = QtWidgets.QPushButton(AlgoCallStmt)
        self.btnCodeArgs.setText("")
        self.btnCodeArgs.setIcon(icon1)
        self.btnCodeArgs.setObjectName("btnCodeArgs")
        self.gridLayout.addWidget(self.btnCodeArgs, 1, 2, 1, 1)
        self.txtArguments = QtWidgets.QLineEdit(AlgoCallStmt)
        self.txtArguments.setObjectName("txtArguments")
        self.gridLayout.addWidget(self.txtArguments, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AlgoCallStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoCallStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.txtFunction)
        self.label_3.setBuddy(self.txtArguments)

        self.retranslateUi(AlgoCallStmt)
        self.buttonBox.accepted.connect(AlgoCallStmt.accept)
        self.buttonBox.rejected.connect(AlgoCallStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoCallStmt)
        AlgoCallStmt.setTabOrder(self.txtFunction, self.txtArguments)
        AlgoCallStmt.setTabOrder(self.txtArguments, self.btnCodeFunc)
        AlgoCallStmt.setTabOrder(self.btnCodeFunc, self.btnCodeArgs)

    def retranslateUi(self, AlgoCallStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoCallStmt.setWindowTitle(_translate("AlgoCallStmt", "Call function"))
        self.label.setText(_translate("AlgoCallStmt", "<html><head/><body><p>Calls the function with the specified arguments.</p><p>The argument list must consist of a comma-separated list of arguments.</p></body></html>"))
        self.label_2.setText(_translate("AlgoCallStmt", "Function:"))
        self.label_3.setText(_translate("AlgoCallStmt", "Arguments:"))

import turing_rc
