# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_mainwindow import Ui_MainWindow
from ui_about import Ui_AboutWindow
import sys
import os
import translator

__version__ = "β-0.2"
__channel__ = "beta"

undo_objs = []

current_file = -1
translate = translator.translate

def getThemedBox():
    msg = QMessageBox()
    msg.setWindowTitle("Turing")
    msg.setStyle(DEFAULT_STYLE)
    msg.setWindowIcon(QIcon("media/icon_16.png"))
    center_widget(msg, window)
    return msg


class myMainWindow(QMainWindow):
    def closeEvent(self, event):
        if False:
            event.accept()
            return
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText(translator.translate("MainWindow", "Do you really want to exit?\nAll unsaved changes will be lost."))
        center_widget(msg, self)
        event.ignore()
        if msg.exec_() == QMessageBox.Yes:
            event.accept()
            exit()


def center_widget(wgt, host):
    if not host:
        host = wgt.parent()

    if host:
        wgt.move(host.geometry().center() - wgt.rect().center())
    else:
        wgt.move(app.desktop().screenGeometry().center() - wgt.rect().center())


def getact(name):
    return getattr(ui, "action" + name)


def refresh():
    refresh_buttons_status()


def handler_Undo():
    translator.load("fr_FR")

def refresh_buttons_status():
    active_code = False
    for c in [
        "Save",
        "SaveAs",
        "Close",
        "Print",
        "Find",
        "Replace",
        "SelectAll",
        "Run",
        "Step",
        "ConvertToPython",
        "ConvertToPseudocode"
    ]:
        getact(c).setEnabled(active_code)

    if current_file != -1:
        getact("Undo").setEnabled(undo_objs[current_file].can_undo())
        getact("Redo").setEnabled(undo_objs[current_file].can_redo())


def handler_Calculator():
    import calculator
    calculator.run()


def handler_Settings():
    import settings
    settings.run()


def handler_HelpContents():
    import help
    help.run()


def handler_AboutTuring():
    about = QDialog()
    about_ui = Ui_AboutWindow()
    about_ui.setupUi(about)
    about_ui.retranslateUi(about)
    about.setFixedSize(about.size())
    txt = about_ui.textBrowser_about.toHtml().replace("{version}", __version__).replace("{channel}", __channel__)
    about_ui.textBrowser_about.setHtml(txt)
    center_widget(about, window)
    about.exec_()


def handler_ShowToolbar():
    if ui.toolBar.isVisible():
        ui.toolBar.hide()
    else:
        ui.toolBar.show()


def handler_ShowToolbarText():
    if ui.toolBar.toolButtonStyle() == Qt.ToolButtonTextUnderIcon:
        ui.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
    else:
        ui.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


def initActions():
    for c in dir(ui):
        if c.startswith("action"):
            name = "handler_" + c[6:]
            if name in globals():
                getattr(ui, c).triggered.connect(globals()[name])


def hnd_language(lng):
    translator.load(lng)
    for a in ui.menuLanguage.actions():
        a.setChecked(a.statusTip() == lng)


def initUi():
    global window, ui
    window = myMainWindow()
    ui = Ui_MainWindow()
    translator.add(ui, window)
    ui.setupUi(window)
    ui.tabWidget.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)
    initActions()
    refresh()

    rightCorner = QMenuBar()
    ui.menubar.removeAction(ui.menuLanguage.menuAction())
    rightCorner.addAction(ui.menuLanguage.menuAction())
    ui.menubar.setCornerWidget(rightCorner)

    gen = lambda a: (lambda: hnd_language(a))
    for a in ui.menuLanguage.actions():
        a.triggered.connect(gen(a.statusTip()))

    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    QCoreApplication.translate2 = QCoreApplication.translate
    QCoreApplication.translate = translator.translate
    DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())
    if os.name == "nt":
        font = QFont("Segoe UI", 9)
        app.setFont(font)
    if False:
        import qdarkstyle

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    initUi()
    hnd_language("en_US")
    exitCode = app.exec_()
    sys.exit(exitCode)
