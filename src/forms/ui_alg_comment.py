# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_alg_comment.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlgoCommentStmt(object):
    def setupUi(self, AlgoCommentStmt):
        AlgoCommentStmt.setObjectName("AlgoCommentStmt")
        AlgoCommentStmt.setWindowModality(QtCore.Qt.WindowModal)
        AlgoCommentStmt.resize(477, 193)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlgoCommentStmt.setWindowIcon(icon)
        AlgoCommentStmt.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlgoCommentStmt)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AlgoCommentStmt)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(AlgoCommentStmt)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(AlgoCommentStmt)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlgoCommentStmt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.lineEdit)

        self.retranslateUi(AlgoCommentStmt)
        self.buttonBox.accepted.connect(AlgoCommentStmt.accept)
        self.buttonBox.rejected.connect(AlgoCommentStmt.reject)
        QtCore.QMetaObject.connectSlotsByName(AlgoCommentStmt)

    def retranslateUi(self, AlgoCommentStmt):
        _translate = QtCore.QCoreApplication.translate
        AlgoCommentStmt.setWindowTitle(_translate("AlgoCommentStmt", "Comment"))
        self.label.setText(_translate("AlgoCommentStmt", "<html><head/><body><p>A comment has no effect whatsoever on the execution of the program.</p><p>It can contain anything.</p></body></html>"))
        self.label_2.setText(_translate("AlgoCommentStmt", "Comment:"))

import turing_rc
