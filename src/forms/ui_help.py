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
        icon.addPixmap(QtGui.QPixmap("media/icon_16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        HelpWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(HelpWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(HelpWindow)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textSearch = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.textSearch.setClearButtonEnabled(False)
        self.textSearch.setObjectName("textSearch")
        self.horizontalLayout.addWidget(self.textSearch)
        self.btnClear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnClear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon1)
        self.btnClear.setObjectName("btnClear")
        self.horizontalLayout.addWidget(self.btnClear)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.listFuncs = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        self.listFuncs.setAnimated(True)
        self.listFuncs.setHeaderHidden(True)
        self.listFuncs.setObjectName("listFuncs")
        self.listFuncs.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.listFuncs)
        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.splitter)
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

