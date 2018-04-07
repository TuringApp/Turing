# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_return.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoReturnStmt(object):
    def setupUi(self, AlgoReturnStmt):
        AlgoReturnStmt.setObjectName("AlgoReturnStmt")
        AlgoReturnStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoReturnStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoReturnStmt.setWindowIcon(icon)
        AlgoReturnStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoReturnStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoReturnStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(AlgoReturnStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtValue = QtWidgets.QLineEdit(AlgoReturnStmt)
        self.txtValue.setEnabled(False)
        self.txtValue.setObjectName("txtValue")
        self.gridLayout.addWidget(self.txtValue, 1, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoReturnStmt)
        self.btnCode.setEnabled(False)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 1, 2, 1, 1)
        self.cbxHasValue = QtWidgets.QCheckBox(AlgoReturnStmt)
        self.cbxHasValue.setObjectName("cbxHasValue")
        self.gridLayout.addWidget(self.cbxHasValue, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoReturnStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AlgoReturnStmt)
        self.buttonBox.accepted.connect(AlgoReturnStmt.accept)
        self.buttonBox.rejected.connect(AlgoReturnStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoReturnStmt)

    def retranslateUi(self, AlgoReturnStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoReturnStmt.setWindowTitle(_translate("AlgoReturnStmt", "Return"))
        self.label.setText(_translate("AlgoReturnStmt", "<html><head/><body><p>Exits the current function and optionally passes a value to the caller.</p></body></html>"))
        self.label_3.setText(_translate("AlgoReturnStmt", "Value:"))
        self.cbxHasValue.setText(_translate("AlgoReturnStmt", "Return a value"))

import turing_rc
