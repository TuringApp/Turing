# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import translator
import util
from ui_about import Ui_AboutWindow
from ui_mainwindow import Ui_MainWindow

translate = QCoreApplication.translate

__version__ = "β-0.2"
__channel__ = "beta"

undo_objs = []

current_file = -1


def get_themed_box():
    msg = QMessageBox()
    msg.setWindowTitle("Turing")
    msg.setStyle(DEFAULT_STYLE)
    msg.setWindowIcon(QIcon("media/icon_16.png"))
    center_widget(msg, window)
    return msg


class MainWindowWrapper(QMainWindow):
    def closeEvent(self, event):
        if False:
            event.accept_token()
            return
        msg = get_themed_box()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText(translate("MainWindow", "Do you really want to exit?\nAll unsaved changes will be lost."))
        center_widget(msg, self)
        event.ignore()
        if msg.exec_() == QMessageBox.Yes:
            try:
                event.accept_token()
            except:
                pass
            exit()


def center_widget(wgt, host):
    if not host:
        host = wgt.parent()

    if host:
        wgt.move(host.geometry().center() - wgt.rect().center())
    else:
        wgt.move(app.desktop().screenGeometry().center() - wgt.rect().center())


def get_action(name):
    return getattr(ui, "action" + name)


def refresh():
    refresh_buttons_status()


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
        get_action(c).setEnabled(active_code)

    if current_file != -1:
        get_action("Undo").setEnabled(undo_objs[current_file].can_undo())
        get_action("Redo").setEnabled(undo_objs[current_file].can_redo())


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


def init_action_handlers():
    for item in dir(ui):
        if item.startswith("action"):
            name = "handler_" + item[6:]

            if name in globals():
                getattr(ui, item).triggered.connect(globals()[name])


def change_language(language):
    translator.load(language)
    for a in ui.menuLanguage.actions():
        a.setChecked(a.statusTip() == language)


def init_ui():
    global window, ui
    window = MainWindowWrapper()
    ui = Ui_MainWindow()
    translator.add(ui, window)
    ui.setupUi(window)
    ui.tabWidget.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)  # hide close button for home
    init_action_handlers()
    refresh()

    right_corner = QMenuBar()
    ui.menubar.removeAction(ui.menuLanguage.menuAction())
    right_corner.addAction(ui.menuLanguage.menuAction())
    ui.menubar.setCornerWidget(right_corner)

    def gen(act):
        return lambda: change_language(act)

    for action in ui.menuLanguage.actions():
        action.triggered.connect(gen(action.statusTip()))

    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    util.translate = translate
    DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())

    if os.name == "nt":
        # fix for ugly font on 7+
        font = QFont("Segoe UI", 9)
        app.setFont(font)

    if False:
        import qdarkstyle

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    init_ui()
    change_language("en_US")

    try:
        exitCode = app.exec_()
    except:
        print("Error: " + str(sys.exc_info()[1]))
        exitCode = 1

    sys.exit(exitCode)
