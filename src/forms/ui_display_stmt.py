# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_display_stmt.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DisplayWindow(object):
    def setupUi(self, DisplayWindow):
        DisplayWindow.setObjectName("DisplayWindow")
        DisplayWindow.resize(671, 402)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/media/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DisplayWindow.setWindowIcon(icon)
        DisplayWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DisplayWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(DisplayWindow)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.label = QtWidgets.QLabel(DisplayWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineInput = QtWidgets.QLineEdit(DisplayWindow)
        self.lineInput.setText("")
        self.lineInput.setObjectName("lineInput")
        self.verticalLayout.addWidget(self.lineInput)
        self.buttonBox = QtWidgets.QDialogButtonBox(DisplayWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DisplayWindow)
        self.buttonBox.accepted.connect(DisplayWindow.accept)
        self.buttonBox.rejected.connect(DisplayWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(DisplayWindow)

    def retranslateUi(self, DisplayWindow):
        _translate = QtCore.QCoreApplication.translate
        DisplayWindow.setWindowTitle(_translate("DisplayWindow", "About Turing"))
        self.label.setText(_translate("DisplayWindow", "Display"))

