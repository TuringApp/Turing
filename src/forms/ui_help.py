# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_help.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(947, 552)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        HelpWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(HelpWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textSearch = QtWidgets.QLineEdit(HelpWindow)
        self.textSearch.setClearButtonEnabled(False)
        self.textSearch.setObjectName("textSearch")
        self.horizontalLayout.addWidget(self.textSearch)
        self.btnClear = QtWidgets.QPushButton(HelpWindow)
        self.btnClear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/media/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon1)
        self.btnClear.setObjectName("btnClear")
        self.horizontalLayout.addWidget(self.btnClear)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.listFuncs = QtWidgets.QTreeWidget(HelpWindow)
        self.listFuncs.setAnimated(True)
        self.listFuncs.setHeaderHidden(True)
        self.listFuncs.setObjectName("listFuncs")
        self.listFuncs.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.listFuncs)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(HelpWindow)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(HelpWindow)
        self.commandLinkButton.setDefault(True)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.verticalLayout_2.addWidget(self.commandLinkButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(HelpWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HelpWindow)
        self.buttonBox.accepted.connect(HelpWindow.accept)
        self.buttonBox.rejected.connect(HelpWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "Help Contents"))
        self.commandLinkButton.setText(_translate("HelpWindow", "CommandLinkButton"))

import turing_rc
