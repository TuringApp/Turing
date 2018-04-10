# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_gpoint.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoGPointStmt(object):
    def setupUi(self, AlgoGPointStmt):
        AlgoGPointStmt.setObjectName("AlgoGPointStmt")
        AlgoGPointStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoGPointStmt.resize(477, 210)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoGPointStmt.setWindowIcon(icon)
        AlgoGPointStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoGPointStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoGPointStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(AlgoGPointStmt)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.txtColor = QtWidgets.QLineEdit(AlgoGPointStmt)
        self.txtColor.setObjectName("txtColor")
        self.gridLayout.addWidget(self.txtColor, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoGPointStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(AlgoGPointStmt)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.btnCodeX = QtWidgets.QPushButton(AlgoGPointStmt)
        self.btnCodeX.setEnabled(True)
        self.btnCodeX.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/edit_line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCodeX.setIcon(icon1)
        self.btnCodeX.setObjectName("btnCodeX")
        self.gridLayout.addWidget(self.btnCodeX, 0, 2, 1, 1)
        self.txtX = QtWidgets.QLineEdit(AlgoGPointStmt)
        self.txtX.setObjectName("txtX")
        self.gridLayout.addWidget(self.txtX, 0, 1, 1, 1)
        self.btnCodeY = QtWidgets.QPushButton(AlgoGPointStmt)
        self.btnCodeY.setEnabled(True)
        self.btnCodeY.setText("")
        self.btnCodeY.setIcon(icon1)
        self.btnCodeY.setObjectName("btnCodeY")
        self.gridLayout.addWidget(self.btnCodeY, 1, 2, 1, 1)
        self.txtY = QtWidgets.QLineEdit(AlgoGPointStmt)
        self.txtY.setObjectName("txtY")
        self.gridLayout.addWidget(self.txtY, 1, 1, 1, 1)
        self.btnCodeColor = QtWidgets.QPushButton(AlgoGPointStmt)
        self.btnCodeColor.setEnabled(True)
        self.btnCodeColor.setText("")
        self.btnCodeColor.setIcon(icon1)
        self.btnCodeColor.setObjectName("btnCodeColor")
        self.gridLayout.addWidget(self.btnCodeColor, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoGPointStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_6.setBuddy(self.txtColor)
        self.label_2.setBuddy(self.txtX)
        self.label_5.setBuddy(self.txtY)

        self.retranslateUi(AlgoGPointStmt)
        self.buttonBox.accepted.connect(AlgoGPointStmt.accept)
        self.buttonBox.rejected.connect(AlgoGPointStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoGPointStmt)
        AlgoGPointStmt.setTabOrder(self.txtX, self.txtY)
        AlgoGPointStmt.setTabOrder(self.txtY, self.txtColor)
        AlgoGPointStmt.setTabOrder(self.txtColor, self.btnCodeX)
        AlgoGPointStmt.setTabOrder(self.btnCodeX, self.btnCodeY)
        AlgoGPointStmt.setTabOrder(self.btnCodeY, self.btnCodeColor)

    def retranslateUi(self, AlgoGPointStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoGPointStmt.setWindowTitle(_translate("AlgoGPointStmt", "Plot point"))
        self.label.setText(_translate("AlgoGPointStmt", "<html><head/><body><p>Draws a point at the specified coordinates.</p><p>The color must be a string containing the color name or RGB hex string.</p></body></html>"))
        self.label_6.setText(_translate("AlgoGPointStmt", "Color:"))
        self.label_2.setText(_translate("AlgoGPointStmt", "X:"))
        self.label_5.setText(_translate("AlgoGPointStmt", "Y:"))

import turing_rc
