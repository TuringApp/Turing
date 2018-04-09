# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_input.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoInputStmt(object):
    def setupUi(self, AlgoInputStmt):
        AlgoInputStmt.setObjectName("AlgoInputStmt")
        AlgoInputStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoInputStmt.resize(477, 240)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoInputStmt.setWindowIcon(icon)
        AlgoInputStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoInputStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoInputStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.txtValue = QtWidgets.QLineEdit(AlgoInputStmt)
        self.txtValue.setEnabled(False)
        self.txtValue.setObjectName("txtValue")
        self.gridLayout.addWidget(self.txtValue, 2, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoInputStmt)
        self.btnCode.setEnabled(False)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 2, 2, 1, 1)
        self.cbxHasValue = QtWidgets.QCheckBox(AlgoInputStmt)
        self.cbxHasValue.setObjectName("cbxHasValue")
        self.gridLayout.addWidget(self.cbxHasValue, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AlgoInputStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(AlgoInputStmt)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.txtVariable = QtWidgets.QLineEdit(AlgoInputStmt)
        self.txtVariable.setObjectName("txtVariable")
        self.gridLayout.addWidget(self.txtVariable, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoInputStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.txtValue)
        self.label_4.setBuddy(self.txtVariable)

        self.retranslateUi(AlgoInputStmt)
        self.buttonBox.accepted.connect(AlgoInputStmt.accept)
        self.buttonBox.rejected.connect(AlgoInputStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoInputStmt)
        AlgoInputStmt.setTabOrder(self.txtVariable, self.cbxHasValue)
        AlgoInputStmt.setTabOrder(self.cbxHasValue, self.txtValue)
        AlgoInputStmt.setTabOrder(self.txtValue, self.btnCode)

    def retranslateUi(self, AlgoInputStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoInputStmt.setWindowTitle(_translate("AlgoInputStmt", "Read user input"))
        self.label.setText(_translate("AlgoInputStmt", "<html><head/><body><p>Asks the user for a value and assigns it to the specified variable.</p><p>Optionally, a message can be displayed. <span style=\" font-weight:600;\">Warning</span>: the message is an expression, thus if you want to display text you need to enclose everything inside quotes.</p></body></html>"))
        self.cbxHasValue.setText(_translate("AlgoInputStmt", "Display a message"))
        self.label_3.setText(_translate("AlgoInputStmt", "Message:"))
        self.label_4.setText(_translate("AlgoInputStmt", "Variable:"))

import turing_rc
