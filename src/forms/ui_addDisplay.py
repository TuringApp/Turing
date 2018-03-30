# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddDisplayWindow(object):
    def setupUi(self, AddDisplayWindow):
        AddDisplayWindow.setObjectName("AddDisplayWindow")
        AddDisplayWindow.resize(671, 402)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/media/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddDisplayWindow.setWindowIcon(icon)
        AddDisplayWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddDisplayWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(AddDisplayWindow)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.label = QtWidgets.QLabel(AddDisplayWindow)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(AddDisplayWindow)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddDisplayWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddDisplayWindow)
        self.buttonBox.accepted.connect(AddDisplayWindow.accept)
        self.buttonBox.rejected.connect(AddDisplayWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(AddDisplayWindow)

    def retranslateUi(self, AddDisplayWindow):
        _translate = QtCore.QCoreApplication.translate
        AddDisplayWindow.setWindowTitle(_translate("AddDisplayWindow", "About Turing"))
        self.label.setText(_translate("AddDisplayWindow", "Display"))

