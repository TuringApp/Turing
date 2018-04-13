# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_sleep.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoSleepStmt(object):
    def setupUi(self, AlgoSleepStmt):
        AlgoSleepStmt.setObjectName("AlgoSleepStmt")
        AlgoSleepStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoSleepStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoSleepStmt.setWindowIcon(icon)
        AlgoSleepStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoSleepStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoSleepStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.txtValue = QtWidgets.QLineEdit(AlgoSleepStmt)
        self.txtValue.setObjectName("txtValue")
        self.gridLayout.addWidget(self.txtValue, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AlgoSleepStmt)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.btnCode = QtWidgets.QPushButton(AlgoSleepStmt)
        self.btnCode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCode.setIcon(icon1)
        self.btnCode.setObjectName("btnCode")
        self.gridLayout.addWidget(self.btnCode, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoSleepStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.txtValue)

        self.retranslateUi(AlgoSleepStmt)
        self.buttonBox.accepted.connect(AlgoSleepStmt.accept)
        self.buttonBox.rejected.connect(AlgoSleepStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoSleepStmt)
        AlgoSleepStmt.setTabOrder(self.txtValue, self.btnCode)

    def retranslateUi(self, AlgoSleepStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoSleepStmt.setWindowTitle(_translate("AlgoSleepStmt", "Wait"))
        self.label.setText(_translate("AlgoSleepStmt", "<html><head/><body><p>Waits for the specified amount of time (in <span style=\" font-weight:600;\">seconds</span>).</p></body></html>"))
        self.label_3.setText(_translate("AlgoSleepStmt", "Duration:"))

import turing_rc
