# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/icon_64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_home = QtWidgets.QWidget()
        self.tab_home.setObjectName("tab_home")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_home)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.tab_home)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_home, icon1, "")
        self.tab_test = QtWidgets.QWidget()
        self.tab_test.setObjectName("tab_test")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_test)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_test)
        font = QtGui.QFont()
        font.setFamily("Linux Biolinum Keyboard O")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser.setFont(font)
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setOverwriteMode(False)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.tabWidget.addTab(self.tab_test, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuR_cents = QtWidgets.QMenu(self.menuFichier)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("media/recent.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuR_cents.setIcon(icon2)
        self.menuR_cents.setObjectName("menuR_cents")
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuAide = QtWidgets.QMenu(self.menubar)
        self.menuAide.setObjectName("menuAide")
        self.menuAffichage = QtWidgets.QMenu(self.menubar)
        self.menuAffichage.setObjectName("menuAffichage")
        self.menuCode = QtWidgets.QMenu(self.menubar)
        self.menuCode.setObjectName("menuCode")
        self.menuOutils = QtWidgets.QMenu(self.menubar)
        self.menuOutils.setObjectName("menuOutils")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dock_settings = QtWidgets.QDockWidget(MainWindow)
        self.dock_settings.setObjectName("dock_settings")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.dockWidgetContents_3)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget_2.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget_2)
        self.dock_settings.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_settings)
        self.dock_output = QtWidgets.QDockWidget(MainWindow)
        self.dock_output.setObjectName("dock_output")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.dockWidgetContents_4)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.dock_output.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dock_output)
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("media/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon3)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("media/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("media/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon5)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("media/save_as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon6)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("media/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionSaveAll = QtWidgets.QAction(MainWindow)
        self.actionSaveAll.setObjectName("actionSaveAll")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("media/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon8)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("media/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon9)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("media/cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon10)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("media/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon11)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("media/paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon12)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("media/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon13)
        self.actionSettings.setObjectName("actionSettings")
        self.actionQuickStart = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("media/quick_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuickStart.setIcon(icon14)
        self.actionQuickStart.setObjectName("actionQuickStart")
        self.actionHelpContents = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("media/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelpContents.setIcon(icon15)
        self.actionHelpContents.setObjectName("actionHelpContents")
        self.actionAboutTuring = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("media/icon_16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAboutTuring.setIcon(icon16)
        self.actionAboutTuring.setObjectName("actionAboutTuring")
        self.actionShowToolbar = QtWidgets.QAction(MainWindow)
        self.actionShowToolbar.setCheckable(True)
        self.actionShowToolbar.setChecked(True)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("media/toolbar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShowToolbar.setIcon(icon17)
        self.actionShowToolbar.setObjectName("actionShowToolbar")
        self.actionExamples = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("media/examples.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExamples.setIcon(icon18)
        self.actionExamples.setObjectName("actionExamples")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("media/print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon19)
        self.actionPrint.setObjectName("actionPrint")
        self.actionFind = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap("media/find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon20)
        self.actionFind.setObjectName("actionFind")
        self.actionReplace = QtWidgets.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap("media/replace.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReplace.setIcon(icon21)
        self.actionReplace.setObjectName("actionReplace")
        self.actionCalculator = QtWidgets.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap("media/calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCalculator.setIcon(icon22)
        self.actionCalculator.setObjectName("actionCalculator")
        self.actionClearRecent = QtWidgets.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap("media/recent_clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClearRecent.setIcon(icon23)
        self.actionClearRecent.setObjectName("actionClearRecent")
        self.actionSelectAll = QtWidgets.QAction(MainWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap("media/select_all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelectAll.setIcon(icon24)
        self.actionSelectAll.setObjectName("actionSelectAll")
        self.actionRun = QtWidgets.QAction(MainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap("media/run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon25)
        self.actionRun.setObjectName("actionRun")
        self.actionStep = QtWidgets.QAction(MainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap("media/step.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStep.setIcon(icon26)
        self.actionStep.setObjectName("actionStep")
        self.actionShowToolbarText = QtWidgets.QAction(MainWindow)
        self.actionShowToolbarText.setCheckable(True)
        self.actionShowToolbarText.setChecked(True)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap("media/toolbar_text.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShowToolbarText.setIcon(icon27)
        self.actionShowToolbarText.setObjectName("actionShowToolbarText")
        self.actionConvertToPython = QtWidgets.QAction(MainWindow)
        self.actionConvertToPython.setObjectName("actionConvertToPython")
        self.actionConvertToPseudocode = QtWidgets.QAction(MainWindow)
        self.actionConvertToPseudocode.setObjectName("actionConvertToPseudocode")
        self.menuR_cents.addSeparator()
        self.menuR_cents.addAction(self.actionClearRecent)
        self.menuFichier.addAction(self.actionNew)
        self.menuFichier.addAction(self.actionOpen)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionSave)
        self.menuFichier.addAction(self.actionSaveAs)
        self.menuFichier.addAction(self.actionSaveAll)
        self.menuFichier.addAction(self.actionClose)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionPrint)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.menuR_cents.menuAction())
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionExit)
        self.menuEdition.addAction(self.actionUndo)
        self.menuEdition.addAction(self.actionRedo)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.actionCut)
        self.menuEdition.addAction(self.actionCopy)
        self.menuEdition.addAction(self.actionPaste)
        self.menuEdition.addSeparator()
        self.menuOptions.addAction(self.actionSettings)
        self.menuAide.addAction(self.actionQuickStart)
        self.menuAide.addAction(self.actionHelpContents)
        self.menuAide.addSeparator()
        self.menuAide.addAction(self.actionExamples)
        self.menuAide.addSeparator()
        self.menuAide.addAction(self.actionAboutTuring)
        self.menuAffichage.addAction(self.actionShowToolbar)
        self.menuAffichage.addAction(self.actionShowToolbarText)
        self.menuCode.addAction(self.actionFind)
        self.menuCode.addAction(self.actionReplace)
        self.menuCode.addSeparator()
        self.menuCode.addAction(self.actionSelectAll)
        self.menuCode.addSeparator()
        self.menuCode.addAction(self.actionRun)
        self.menuCode.addAction(self.actionStep)
        self.menuCode.addSeparator()
        self.menuCode.addAction(self.actionConvertToPython)
        self.menuCode.addAction(self.actionConvertToPseudocode)
        self.menuOutils.addAction(self.actionCalculator)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuAffichage.menuAction())
        self.menubar.addAction(self.menuCode.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuOutils.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addAction(self.actionFind)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStep)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Turing"))
        self.label.setText(_translate("MainWindow", "<h1>Bienvenue dans Turing</h1>\n"
""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_home), _translate("MainWindow", "Accueil"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Linux Biolinum Keyboard O\'; font-size:20pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#55ff55;\">soin</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_test), _translate("MainWindow", "Tab test"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuR_cents.setTitle(_translate("MainWindow", "Récents"))
        self.menuEdition.setTitle(_translate("MainWindow", "Edition"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuAide.setTitle(_translate("MainWindow", "Aide"))
        self.menuAffichage.setTitle(_translate("MainWindow", "Affichage"))
        self.menuCode.setTitle(_translate("MainWindow", "Programme"))
        self.menuOutils.setTitle(_translate("MainWindow", "Outils"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dock_settings.setWindowTitle(_translate("MainWindow", "Outils"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.dock_output.setWindowTitle(_translate("MainWindow", "Sortie"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Voici la carte kiwiii</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.actionNew.setText(_translate("MainWindow", "Nouveau"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Ouvrir"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Enregistrer"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSaveAs.setText(_translate("MainWindow", "Enregistrer sous"))
        self.actionClose.setText(_translate("MainWindow", "Fermer"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionExit.setText(_translate("MainWindow", "Quitter"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSaveAll.setText(_translate("MainWindow", "Enregistrer tout"))
        self.actionSaveAll.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionUndo.setText(_translate("MainWindow", "Annuler"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Rétablir"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionCut.setText(_translate("MainWindow", "Couper"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copier"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Coller"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionSettings.setText(_translate("MainWindow", "Préférences"))
        self.actionQuickStart.setText(_translate("MainWindow", "Tutoriel rapide"))
        self.actionHelpContents.setText(_translate("MainWindow", "Pages d\'aide"))
        self.actionHelpContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAboutTuring.setText(_translate("MainWindow", "À propos de Turing"))
        self.actionShowToolbar.setText(_translate("MainWindow", "Barre d\'outils"))
        self.actionExamples.setText(_translate("MainWindow", "Exemples"))
        self.actionPrint.setText(_translate("MainWindow", "Imprimer"))
        self.actionPrint.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionFind.setText(_translate("MainWindow", "Rechercher"))
        self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionReplace.setText(_translate("MainWindow", "Remplacer"))
        self.actionReplace.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionCalculator.setText(_translate("MainWindow", "Calculatrice"))
        self.actionClearRecent.setText(_translate("MainWindow", "Effacer"))
        self.actionSelectAll.setText(_translate("MainWindow", "Sélectionner tout"))
        self.actionSelectAll.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionRun.setText(_translate("MainWindow", "Exécuter"))
        self.actionRun.setShortcut(_translate("MainWindow", "F5"))
        self.actionStep.setText(_translate("MainWindow", "Pas-à-pas"))
        self.actionStep.setShortcut(_translate("MainWindow", "F10"))
        self.actionShowToolbarText.setText(_translate("MainWindow", "Texte des icônes"))
        self.actionConvertToPython.setText(_translate("MainWindow", "Convertir en Python"))
        self.actionConvertToPseudocode.setText(_translate("MainWindow", "Convertir en pseudocode"))

