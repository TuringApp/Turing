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
        icon.addPixmap(QtGui.QPixmap(":/action/media/calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CalcWindow.setWindowIcon(icon)
        CalcWindow.setIconSize(QtCore.QSize(16, 16))
        self.centralwidget = QtWidgets.QWidget(CalcWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lstHistory = QtWidgets.QListWidget(self.centralwidget)
        self.lstHistory.setObjectName("lstHistory")
        self.verticalLayout.addWidget(self.lstHistory)
        CalcWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CalcWindow)
        QtCore.QMetaObject.connectSlotsByName(CalcWindow)

    def retranslateUi(self, CalcWindow):
        _translate = QtCore.QCoreApplication.translate
        CalcWindow.setWindowTitle(_translate("CalcWindow", "Calculator"))

import turing_rc
