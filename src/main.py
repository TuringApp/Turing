# -*- coding: utf-8 -*-

import datetime
import html
import os
import runpy
import sys
import tempfile

import pyqode.python.backend
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
import pygments.styles
import editor_backend
import util
import util.code
import util.html
from forms.ui_mainwindow import Ui_MainWindow
from lang import translator
from util.widgets import center_widget

translate = QCoreApplication.translate

__version__ = "β-0.2"
__channel__ = "beta"

undo = None
mode_python = False
code_editor = None
panel_search = None
current_output = ""
after_output = ""
user_input = None
syntax_highlighter = None
editor_action_table = [
    ("Copy", "copy"),
    ("Cut", "cut"),
    ("Paste", "paste"),
    ("Undo", "undo"),
    ("Redo", "redo"),
    ("SelectAll", "select_all"),
    ("DuplicateLine", "duplicate_line"),
    ("Indent", "indent"),
    ("Unindent", "un_indent"),
    ("GoToLine", "goto_line"),
    ("Find", "Search"),
    ("Replace", "ActionSearchAndReplace"),
    ("FindPrevious", "FindPrevious"),
    ("FindNext", "FindNext")
]
python_only = [
    "SelectAll",
    "Find",
    "FindPrevious",
    "FindNext",
    "Replace",
    "Indent",
    "Unindent"
]


def get_themed_box():
    msg = QMessageBox()
    msg.setWindowTitle("Turing")
    msg.setStyle(DEFAULT_STYLE)
    msg.setWindowIcon(QIcon(":/icon/media/icon.ico"))
    center_widget(msg, window)
    return msg


def sleep(duration: int):
    duration *= 1000
    begin = datetime.datetime.now()
    while (datetime.datetime.now() - begin).microseconds < duration:
        QCoreApplication.processEvents()


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


def get_action(name: str) -> QAction:
    return getattr(ui, "action" + name)


def refresh():
    refresh_buttons_status()


def refresh_buttons_status():
    if mode_python:
        for ours, theirs in editor_action_table:
            get_action(ours).setEnabled(getattr(code_editor, "action_" + theirs).isEnabled())

    active_code = True
    for c in [
        "Save",
        "SaveAs",
        "Close",
        "Print",
        "Find",
        "Replace",
        "Run",
        "Step",
        "ConvertToPython",
        "ConvertToPseudocode"
    ]:
        get_action(c).setEnabled(active_code)

    for c in python_only:
        get_action(c).setVisible(mode_python)

    # if current_file != -1:
    #    get_action("Undo").setEnabled(undo_objs[current_file].can_undo())
    #    get_action("Redo").setEnabled(undo_objs[current_file].can_redo())


def handler_Undo():
    if mode_python:
        code_editor.undo()


def handler_Redo():
    if mode_python:
        code_editor.redo()


def handler_SelectAll():
    code_editor.selectAll()


def handler_Cut():
    if mode_python:
        code_editor.cut()


def handler_Copy():
    if mode_python:
        code_editor.copy()


def handler_Paste():
    if mode_python:
        code_editor.paste()


def handler_DuplicateLine():
    if mode_python:
        code_editor.duplicate_line()


def handler_Indent():
    code_editor.indent()


def handler_Unindent():
    code_editor.un_indent()


def handler_GoToLine():
    code_editor.goto_line()


def handler_Find():
    panel_search.on_search()


def handler_FindPrevious():
    panel_search.select_previous()


def handler_FindNext():
    panel_search.select_next()


def handler_Replace():
    panel_search.on_search_and_replace()


def handler_Calculator():
    from forms import calculator
    calculator.run()


def handler_Settings():
    from forms import settings
    settings.run()


def handler_HelpContents():
    from forms import help
    help.run()


def python_print(*args, end="\n"):
    global current_output
    current_output += html.escape(" ".join(str(arg) for arg in args))
    current_output += end
    update_output()


def update_output():
    ui.txtOutput.setHtml("<pre>%s</pre>" % (current_output + after_output))
    ui.txtOutput.moveCursor(QTextCursor.End)
    ui.txtOutput.ensureCursorVisible()


def python_input(prompt=""):
    python_print(prompt, end="")

    global after_output
    after_output = "<hr>"
    after_output += util.html.centered(
        "<h3>%s</h3>" % util.html.color_span("<i>%s</i>" % translate("MainWindow", "Input: ") + html.escape(prompt),
                                             "red"))
    update_output()

    ui.btnSendInput.setEnabled(True)
    ui.txtInput.setEnabled(True)

    for n in range(3):
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ffbaba; }")
        sleep(50)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
        sleep(50)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff5252; }")
        sleep(50)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
        sleep(50)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ffbaba; }")
        sleep(50)
        ui.txtInput.setStyleSheet("")
        sleep(200)

    global user_input
    user_input = None

    while user_input is None:
        QCoreApplication.processEvents()

    ui.btnSendInput.setEnabled(False)
    ui.txtInput.setEnabled(False)
    ui.txtInput.setText("")

    after_output = ""
    python_print(user_input)

    return user_input


def python_print_error(msg):
    global current_output
    current_output += util.html.color_span(msg, "red")
    update_output()


def handler_Run():
    ui.actionRun.setDisabled(True)
    ui.actionStep.setDisabled(True)
    file = tempfile.NamedTemporaryFile(mode="w+b", suffix=".py", delete=False)
    try:
        code = util.code.python_wrapper(code_editor.toPlainText()).encode("utf8")
        file.write(code)
        file.close()
        runpy.run_path(file.name, init_globals={"print": python_print, "input": python_input})
    except SyntaxError as err:
        msg = translate("MainWindow", "Syntax error ({type}) at line {line}, offset {off}: ").format(
            type=type(err).__name__, line=err.lineno - 10, off=err.offset)
        python_print_error(msg + err.text)
        python_print_error(" " * (len(msg) + err.offset - 1) + "↑")
    except:
        python_print_error(str(sys.exc_info()[1]))
    finally:
        os.unlink(file.name)
        global current_output
        current_output += util.html.centered(util.html.color_span(translate("MainWindow", "end of output"), "red"))
        current_output += "<hr>"
        update_output()
        ui.actionRun.setDisabled(False)
        ui.actionStep.setDisabled(False)


def handler_AboutTuring():
    from forms import about
    about.run(window, __version__, __channel__)


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


def copy_action(source: QAction, target: QAction):
    target.setText(source.text())
    target.setIcon(source.icon())


def change_language(language: str):
    translator.load(language)
    load_editor_actions()
    for a in ui.menuLanguage.actions():
        a.setChecked(a.statusTip() == language)


def send_user_input():
    global user_input
    user_input = ui.txtInput.text()


def clear_output():
    global current_output
    current_output = ""
    update_output()


def print_output():
    print("\n".join(dir(code_editor)))
    pass


def load_editor_actions():
    for ours, theirs in editor_action_table:
        copy_action(getattr(ui, "action" + ours), getattr(code_editor, "action_" + theirs))


def copy_actions_to_editor(panel):
    for name, obj in panel.__dict__.items():
        if name.startswith("action_"):
            setattr(code_editor, name, obj)
        elif name.startswith("action"):  # workaround for shitty naming by the devs
            setattr(code_editor, "action_" + name[6:], obj)


def setStyle(style):
    syntax_highlighter.pygments_style = style

    for act in ui.menuChangeStyle.actions():
        act.setChecked(act.text() == style)


def load_code_editor():
    global code_editor
    code_editor = api.CodeEdit()
    code_editor.backend.start(editor_backend.__file__)

    code_editor.modes.append(modes.CodeCompletionMode())
    code_editor.modes.append(modes.CaretLineHighlighterMode())
    code_editor.modes.append(modes.AutoCompleteMode())
    code_editor.modes.append(modes.IndenterMode())
    code_editor.modes.append(modes.AutoIndentMode())
    code_editor.modes.append(modes.OccurrencesHighlighterMode())
    code_editor.modes.append(modes.SmartBackSpaceMode())
    code_editor.modes.append(modes.SymbolMatcherMode())
    code_editor.modes.append(modes.ZoomMode())
    code_editor.modes.append(modes.ExtendedSelectionMode())

    global syntax_highlighter
    syntax_highlighter = code_editor.modes.append(modes.PygmentsSyntaxHighlighter(code_editor.document()))
    syntax_highlighter.fold_detector = api.IndentFoldDetector()

    code_editor.panels.append(panels.FoldingPanel())
    code_editor.panels.append(panels.LineNumberPanel())
    code_editor.modes.append(modes.CheckerMode(pyqode.python.backend.run_pep8))
    code_editor.panels.append(panels.GlobalCheckerPanel(), panels.GlobalCheckerPanel.Position.LEFT)
    global panel_search
    panel_search = code_editor.panels.append(panels.SearchAndReplacePanel(), api.Panel.Position.BOTTOM)
    copy_actions_to_editor(panel_search)

    code_editor.textChanged.connect(refresh)

    load_editor_actions()

    def gen(s):
        return lambda: setStyle(s)

    for style in pygments.styles.get_all_styles():
        action = QAction(window)
        action.setText(style)
        action.setCheckable(True)
        action.triggered.connect(gen(style))
        ui.menuChangeStyle.addAction(action)

    ui.verticalLayout_8.addWidget(code_editor)


def init_ui():
    global window, ui
    window = MainWindowWrapper()
    ui = Ui_MainWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    load_code_editor()
    init_action_handlers()
    refresh()

    right_corner = QMenuBar()
    ui.menubar.removeAction(ui.menuLanguage.menuAction())
    right_corner.addAction(ui.menuLanguage.menuAction())
    ui.menubar.setCornerWidget(right_corner)

    ui.btnSendInput.clicked.connect(send_user_input)
    ui.btnClearOutput.clicked.connect(clear_output)
    ui.btnPrintOutput.clicked.connect(print_output)

    def gen(act):
        return lambda: change_language(act)

    for action in ui.menuLanguage.actions():
        action.triggered.connect(gen(action.statusTip()))

    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Turing")
    app.setApplicationVersion(__version__)

    util.translate_backend = translate
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
        print(translate("MainWindow", "Error: ") + str(sys.exc_info()[1]))
        exitCode = 1

    sys.exit(exitCode)
