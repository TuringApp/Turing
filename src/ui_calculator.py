# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_calculator.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CalcWindow(object):
    def setupUi(self, CalcWindow):
        CalcWindow.setObjectName("CalcWindow")
        CalcWindow.resize(348, 407)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CalcWindow.setWindowIcon(icon)
        CalcWindow.setIconSize(QtCore.QSize(16, 16))
        self.centralwidget = QtWidgets.QWidget(CalcWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lstHistory = QtWidgets.QListWidget(self.centralwidget)
        self.lstHistory.setObjectName("lstHistory")
        self.verticalLayout.addWidget(self.lstHistory)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtExpr = QtWidgets.QLineEdit(self.centralwidget)
        self.txtExpr.setObjectName("txtExpr")
        self.horizontalLayout.addWidget(self.txtExpr)
        self.btnCalc = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalc.setObjectName("btnCalc")
        self.horizontalLayout.addWidget(self.btnCalc)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbxFuncs = QtWidgets.QComboBox(self.centralwidget)
        self.cbxFuncs.setObjectName("cbxFuncs")
        self.verticalLayout_2.addWidget(self.cbxFuncs)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.btnInsFunc = QtWidgets.QPushButton(self.centralwidget)
        self.btnInsFunc.setEnabled(False)
        self.btnInsFunc.setObjectName("btnInsFunc")
        self.verticalLayout_2.addWidget(self.btnInsFunc)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        CalcWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CalcWindow)
        QtCore.QMetaObject.connectSlotsByName(CalcWindow)

    def retranslateUi(self, CalcWindow):
        _translate = QtCore.QCoreApplication.translate
        CalcWindow.setWindowTitle(_translate("CalcWindow", "Calculatrice"))
        self.btnCalc.setText(_translate("CalcWindow", "="))
        self.btnInsFunc.setText(_translate("CalcWindow", "Insérer"))
        self.pushButton_2.setText(_translate("CalcWindow", "PushButton"))

