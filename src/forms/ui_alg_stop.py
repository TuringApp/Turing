# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_stop.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoStopStmt(object):
    def setupUi(self, AlgoStopStmt):
        AlgoStopStmt.setObjectName("AlgoStopStmt")
        AlgoStopStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoStopStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoStopStmt.setWindowIcon(icon)
        AlgoStopStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoStopStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoStopStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(AlgoStopStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtMessage = QtWidgets.QLineEdit(AlgoStopStmt)
        self.txtMessage.setEnabled(False)
        self.txtMessage.setObjectName("txtMessage")
        self.gridLayout.addWidget(self.txtMessage, 1, 1, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoStopStmt)
        self.btnCode.setEnabled(False)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 1, 2, 1, 1)
        self.cbxHasValue = QtWidgets.QCheckBox(AlgoStopStmt)
        self.cbxHasValue.setObjectName("cbxHasValue")
        self.gridLayout.addWidget(self.cbxHasValue, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoStopStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.txtMessage)

        self.retranslateUi(AlgoStopStmt)
        self.buttonBox.accepted.connect(AlgoStopStmt.accept)
        self.buttonBox.rejected.connect(AlgoStopStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoStopStmt)
        AlgoStopStmt.setTabOrder(self.txtMessage, self.cbxHasValue)
        AlgoStopStmt.setTabOrder(self.cbxHasValue, self.btnCode)

    def retranslateUi(self, AlgoStopStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoStopStmt.setWindowTitle(_translate("AlgoStopStmt", "Breakpoint"))
        self.label.setText(_translate("AlgoStopStmt", "<html><head/><body><p>Pauses the program until &quot;Run&quot; or &quot;Debug&quot; is pressed.</p></body></html>"))
        self.label_3.setText(_translate("AlgoStopStmt", "Message:"))
        self.cbxHasValue.setText(_translate("AlgoStopStmt", "Display a message"))

import turing_rc
