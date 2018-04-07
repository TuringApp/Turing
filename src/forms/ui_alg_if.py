# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_if.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoIfStmt(object):
    def setupUi(self, AlgoIfStmt):
        AlgoIfStmt.setObjectName("AlgoIfStmt")
        AlgoIfStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoIfStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoIfStmt.setWindowIcon(icon)
        AlgoIfStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoIfStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoIfStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(AlgoIfStmt)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoIfStmt)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoIfStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoIfStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AlgoIfStmt)
        self.buttonBox.accepted.connect(AlgoIfStmt.accept)
        self.buttonBox.rejected.connect(AlgoIfStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoIfStmt)

    def retranslateUi(self, AlgoIfStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoIfStmt.setWindowTitle(_translate("AlgoIfStmt", "Display value"))
        self.label.setText(_translate("AlgoIfStmt", "<html><head/><body><p>Checks if the specified condition is true.</p><p>The block will only be executed if the condition is true, otherwise the program will continue with the instruction following the block.</p></body></html>"))
        self.label_2.setText(_translate("AlgoIfStmt", "Condition:"))

import turing_rc
