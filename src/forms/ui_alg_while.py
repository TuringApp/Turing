# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_while.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoWhileStmt(object):
    def setupUi(self, AlgoWhileStmt):
        AlgoWhileStmt.setObjectName("AlgoWhileStmt")
        AlgoWhileStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoWhileStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoWhileStmt.setWindowIcon(icon)
        AlgoWhileStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoWhileStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoWhileStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(AlgoWhileStmt)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoWhileStmt)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoWhileStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoWhileStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.lineEdit)

        self.retranslateUi(AlgoWhileStmt)
        self.buttonBox.accepted.connect(AlgoWhileStmt.accept)
        self.buttonBox.rejected.connect(AlgoWhileStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoWhileStmt)

    def retranslateUi(self, AlgoWhileStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoWhileStmt.setWindowTitle(_translate("AlgoWhileStmt", "WHILE loop"))
        self.label.setText(_translate("AlgoWhileStmt", "<html><head/><body><p>Executes the instructions while the condition is true.</p><p>As soon as the condition is false, the program continues with the instruction following the block.</p></body></html>"))
        self.label_2.setText(_translate("AlgoWhileStmt", "Condition:"))

import turing_rc
