# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_display.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoDisplayStmt(object):
    def setupUi(self, AlgoDisplayStmt):
        AlgoDisplayStmt.setObjectName("AlgoDisplayStmt")
        AlgoDisplayStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoDisplayStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoDisplayStmt.setWindowIcon(icon)
        AlgoDisplayStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoDisplayStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoDisplayStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(AlgoDisplayStmt)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoDisplayStmt)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoDisplayStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoDisplayStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AlgoDisplayStmt)
        self.buttonBox.accepted.connect(AlgoDisplayStmt.accept)
        self.buttonBox.rejected.connect(AlgoDisplayStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoDisplayStmt)

    def retranslateUi(self, AlgoDisplayStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoDisplayStmt.setWindowTitle(_translate("AlgoDisplayStmt", "Display value"))
        self.label.setText(_translate("AlgoDisplayStmt", "<html><head/><body><p>Displays a value in the output window. </p><p>The value can be of any type, it will be automatically converted to a textual representation.</p></body></html>"))
        self.label_2.setText(_translate("AlgoDisplayStmt", "Value:"))

import turing_rc
