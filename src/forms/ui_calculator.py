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
        CalcWindow.resize(671, 601)
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
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon1)
        self.btnClear.setObjectName("btnClear")
        self.horizontalLayout.addWidget(self.btnClear)
        self.btnCalc = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalc.setText("")
        self.btnCalc.setIcon(icon)
        self.btnCalc.setObjectName("btnCalc")
        self.horizontalLayout.addWidget(self.btnCalc)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbxFuncs = QtWidgets.QComboBox(self.centralwidget)
        self.cbxFuncs.setObjectName("cbxFuncs")
        self.verticalLayout_2.addWidget(self.cbxFuncs)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        CalcWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CalcWindow)
        QtCore.QMetaObject.connectSlotsByName(CalcWindow)

    def retranslateUi(self, CalcWindow):
        _translate = QtCore.QCoreApplication.translate
        CalcWindow.setWindowTitle(_translate("CalcWindow", "Calculator"))

