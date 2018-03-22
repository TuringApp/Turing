# -*- coding: utf-8 -*-

import datetime
import html
import os
import runpy
import sys
import tempfile
import threading
import traceback
from typing import Optional

import pygments.styles
import pyqode.python.backend
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels

import editor_backend
import util
import util.code
import util.html
from algo.stmts import *
from algo.worker import Worker
from forms.ui_mainwindow import Ui_MainWindow
from lang import translator
from maths.parser import quick_parse as parse
from util.widgets import center_widget, QClickableLabel

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

worker = None
algo = BlockStmt([])
item_map = {}
root_item = None

block_html = '<span style="color:darkred;font-weight:bold">'
keyword_html = '<span style="color:blue;font-weight:bold">'
comment_html = '<span style="color:darkgreen;font-style:italic">'

running = False


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
    global current_output
    ui.txtOutput.setHtml("<pre>%s</pre>" % (current_output + after_output))
    ui.txtOutput.moveCursor(QTextCursor.End)
    ui.txtOutput.ensureCursorVisible()
    if current_output.endswith("\n\n"):
        current_output = current_output[:-1]


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


def init_worker():
    global worker
    worker = Worker(algo.children)
    worker.callback_print = python_print
    worker.callback_input = python_input
    worker.init()


def end_output():
    global current_output
    current_output += util.html.centered(util.html.color_span(translate("MainWindow", "end of output"), "red"))
    current_output += "<hr>"
    update_output()


def set_current_line(current: Optional[BaseStmt]):
    for item, stmt in item_map.values():
        if stmt == current:
            item.setBackground(0, QBrush(QColor("red")))
        else:
            item.setBackground(0, root_item.background(0))


def handler_Step():
    ui.actionRun.setDisabled(True)
    ui.actionStep.setDisabled(True)
    global running, current

    try:
        if mode_python:
            pass
        else:
            if running:
                worker.exec_stmt(current)
            else:
                init_worker()
                running = True

            current = worker.next_stmt()

            set_current_line(current)
    except:
        show_error()
    finally:
        if worker.finished:
            end_output()

            running = False
        ui.actionRun.setDisabled(False)
        ui.actionStep.setDisabled(False)


def handler_Run():
    ui.actionRun.setDisabled(True)
    ui.actionStep.setDisabled(True)
    global running

    try:
        if mode_python:
            file = tempfile.NamedTemporaryFile(mode="w+b", suffix=".py", delete=False)
            try:
                code = util.code.python_wrapper(code_editor.toPlainText()).encode("utf8")
                file.write(code)
                file.close()
                running = True
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
        else:
            if not running:
                init_worker()
                running = True
            else:
                worker.exec_stmt(current)
                set_current_line(None)

            while not worker.finished:
                worker.step()
    except:
        show_error()
    finally:
        end_output()
        ui.actionRun.setDisabled(False)
        ui.actionStep.setDisabled(False)
        running = False


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
    refresh_algo_text()


def send_user_input():
    global user_input
    user_input = ui.txtInput.text()


def clear_output():
    global current_output
    current_output = ""
    if not mode_python:
        set_current_line(None)
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

    setStyle("default")

    ui.verticalLayout_8.addWidget(code_editor)


def get_item_label(item):
    def gen_func(item):
        return lambda: ui.treeWidget.setCurrentItem(item)

    txt = QClickableLabel()
    txt.setStyleSheet(ui.treeWidget.styleSheet())
    txt.clicked.connect(gen_func(item))
    item.lbl = txt
    ui.treeWidget.setItemWidget(item, 0, txt)

    return txt


def get_item_html(html, data=""):
    item = QTreeWidgetItem()
    item.setStatusTip(0, data)

    lbl = get_item_label(item)
    lbl.setText('&nbsp;<span>%s</span>' % html)

    ui.treeWidget.setItemWidget(item, 0, lbl)

    return (item, lbl)


def refresh_algo_text():
    for item, stmt in item_map.values():
        lbl = get_item_label(item)
        lbl.setText('&nbsp;<span>%s</span>' % str_stmt(stmt))


def add_display():
    append_line(DisplayStmt(parse("\"hello world\"")))


def add_def_variable():
    pass


def add_input():
    pass


def add_call():
    pass


def add_def_func():
    pass


def add_return():
    pass


def add_if_block():
    pass


def add_else_block():
    append_line(ElseStmt([]))


def add_for_loop():
    pass


def add_while_loop():
    pass


def add_break_stmt():
    append_line(BreakStmt())


def add_continue_stmt():
    append_line(ContinueStmt())


def add_stop_stmt():
    append_line(StopStmt())


def add_comment_stmt():
    append_line(CommentStmt("sample comment"))


def btn_add_line():
    append_line(BaseStmt())


def btn_delete_line():
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)

    if isinstance(parent_stmt.children[current_pos[-1]], IfStmt) and current_pos[-1] < len(
            parent_stmt.children) - 1 and isinstance(parent_stmt.children[current_pos[-1] + 1], ElseStmt):
        del parent_stmt.children[current_pos[-1] + 1]

    del parent_stmt.children[current_pos[-1]]

    refresh_algo()
    algo_sel_changed()


def btn_edit_line():
    pass


def btn_move_up_block():
    btn_move_up(True)


def btn_move_up(block=False):
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)
    current_pos[-1] -= 1

    if current_pos[-1] < 0:
        current_pos.pop()
    else:
        if not block:
            existing = parent_stmt.children[current_pos[-1]]
            if isinstance(existing, BlockStmt):
                current_pos.append(len(existing.children))

    move_line(get_current_pos(), current_pos)


def btn_move_down_block():
    btn_move_down(True)


def btn_move_down(block=False):
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)
    current_pos[-1] += 1

    if current_pos[-1] >= len(parent_stmt.children):
        current_pos.pop()
        current_pos[-1] += 1
    else:
        if not block:
            existing = parent_stmt.children[current_pos[-1]]
            if isinstance(existing, BlockStmt):
                current_pos.append(0)

    move_line(get_current_pos(), current_pos)


def append_line(stmt):
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)
    if current_pos != []:
        existing = parent_stmt.children[current_pos[-1]]
        if type(existing) == BaseStmt:
            parent_stmt.children[current_pos[-1]] = stmt
            refresh_algo()
            return
    else:
        existing = algo

    if isinstance(existing, BlockStmt):
        current_pos.append(0)
    else:
        current_pos[-1] += 1
    add_line(current_pos, stmt)


def get_current_stmt():
    current_item = ui.treeWidget.currentItem()
    for item, stmt in item_map.values():
        if item == current_item:
            return stmt

    return None


def get_current_pos():
    current = []
    found = False
    current_stmt = get_current_stmt()

    def find_block(block: BlockStmt):
        nonlocal found
        if found:
            return

        nonlocal current
        current.append(0)

        for child in block.children:
            if child == current_stmt:
                found = True
                return

            if isinstance(child, BlockStmt):
                find_block(child)
                if found:
                    return

            current[-1] += 1

        current.pop()

    if current_stmt is not None:
        find_block(algo)

    return current


def get_parent(pos):
    parent = root_item
    parent_stmt = algo

    for p in pos[:-1]:
        parent = parent.child(p)
        parent_stmt = parent_stmt.children[p]

    return parent, parent_stmt


def refresh_algo():
    current = None
    line = ui.treeWidget.currentItem()
    for item, stmt in item_map.values():
        if item == line:
            current = stmt
            break

    load_block(algo)

    for item, stmt in item_map.values():
        if stmt == current:
            ui.treeWidget.setCurrentItem(item)
            break


def move_line(old_pos, new_pos):
    _, old_parent_stmt = get_parent(old_pos)
    _, new_parent_stmt = get_parent(new_pos)

    line = old_parent_stmt.children[old_pos[-1]]
    del old_parent_stmt.children[old_pos[-1]]
    new_parent_stmt.children.insert(new_pos[-1], line)

    refresh_algo()


def add_line(pos, stmt, add=True):
    parent, parent_stmt = get_parent(pos)

    item, lbl = get_item_html(str_stmt(stmt))

    parent.insertChild(pos[-1], item)
    if add:
        parent_stmt.children.insert(pos[-1], stmt)

    store_line(item, stmt)

    ui.treeWidget.setItemWidget(item, 0, lbl)


def str_stmt(stmt):
    if isinstance(stmt, DisplayStmt):
        ret = translate("Algo", "[k]DISPLAY[/k] [c]{val}[/c]").format(val=stmt.content.code())

    elif isinstance(stmt, BreakStmt):
        ret = translate("Algo", "[k]BREAK[/k]")

    elif isinstance(stmt, ContinueStmt):
        ret = translate("Algo", "[k]CONTINUE[/k]")

    elif isinstance(stmt, ElseStmt):
        ret = translate("Algo", "[b]ELSE[/b]")

    elif isinstance(stmt, WhileStmt):
        ret = translate("Algo", "[b]WHILE[/b] [c]{cond}[/c]").format(cond=stmt.condition.code())

    elif isinstance(stmt, IfStmt):
        ret = translate("Algo", "[b]IF[/b] [c]{cond}[/c]").format(cond=stmt.condition.code())

    elif isinstance(stmt, InputStmt):
        ret = translate("Algo", "[k]INPUT[/k] [c]{prompt}[/c] [k]TO[/k] [c]{var}[/c]").format(
            prompt="" if stmt.prompt is None else stmt.prompt.code(), var=stmt.variable)

    elif isinstance(stmt, AssignStmt):
        if stmt.value is None:
            ret = translate("Algo", "[k]DECLARE[/k] [c]{var}[/c]").format(var=stmt.variable)
        else:
            ret = translate("Algo", "[k]ASSIGN[/k] [c]{var}[/c] = [c]{value}[/c]").format(var=stmt.variable,
                                                                                          value=stmt.value.code())

    elif isinstance(stmt, CallStmt):
        ret = translate("Algo", "[k]CALL[/k] [c]{code}[/c]").format(code=stmt.to_node().code())

    elif isinstance(stmt, ForStmt):
        ret = translate("Algo",
                        "[b]FOR[/b] [c]{var}[/c] [b]FROM[/b] [c]{begin}[/c] [b]TO[/b] [c]{end}[/c] {step}").format(
            var=stmt.variable, begin=stmt.begin.code(), end=stmt.end.code(),
            step="" if stmt.step is None else translate("Algo", "([b]STEP[/b] [c]{step}[/c])").format(
                step=stmt.step.code()))

    elif isinstance(stmt, FuncStmt):
        ret = translate("Algo", "[b]FUNCTION[/b] [c]{func}({args})[/c]").format(func=stmt.name,
                                                                                args=", ".join(stmt.parameters))

    elif isinstance(stmt, ReturnStmt):
        ret = translate("Algo", "[k]RETURN[/k] [c]{val}[/c]").format(
            val="" if stmt.value is None else stmt.value.code())

    elif isinstance(stmt, StopStmt):
        ret = translate("Algo", "[k]STOP[/k]")

    elif isinstance(stmt, CommentStmt):
        ret = "[t]{com}[/t]".format(com=stmt.content)

    elif isinstance(stmt, BlockStmt):
        ret = translate("Algo", "[b]PROGRAM[/b]")

    elif isinstance(stmt, BaseStmt):
        ret = translate("Algo", "[i]empty[/i]")

    else:
        ret = "unimpl %s" % stmt

    ret = ret.replace("[b]", block_html).replace("[/b]", "</span>")
    ret = ret.replace("[k]", keyword_html).replace("[/k]", "</span>")
    ret = ret.replace("[c]", "<code>").replace("[/c]", "</code>")
    ret = ret.replace("[i]", "<i>").replace("[/i]", "</i>")
    ret = ret.replace("[t]", comment_html).replace("[/t]", "</span>")
    ret = ret.replace("  ", " ")

    return ret.strip()


def store_line(item: QTreeWidgetItem, stmt: BaseStmt):
    item_map[id(stmt)] = item, stmt


def load_block(stmt: BlockStmt):
    global item_map
    item_map = {}
    item_labels = {}
    ui.treeWidget.clear()

    global root_item, algo
    algo = stmt
    root_item, lbl = get_item_html(str_stmt(algo))
    ui.treeWidget.addTopLevelItem(root_item)
    store_line(root_item, algo)
    ui.treeWidget.setItemWidget(root_item, 0, lbl)

    current = []

    def add_block(block: BlockStmt):
        nonlocal current
        current.append(0)

        for child in block.children:
            add_line(current, child, add=False)

            if isinstance(child, BlockStmt):
                add_block(child)

            current[-1] += 1

        current.pop()

    add_block(stmt)

    ui.treeWidget.expandAll()


def load_algo():
    load_block(BlockStmt([
        ForStmt("i", parse("1"), parse("16"), [
            IfStmt(parse("i % 15 == 0"), [
                DisplayStmt(parse("\"FizzBuzz\""))
            ]),
            ElseStmt([
                IfStmt(parse("i % 3 == 0"), [
                    DisplayStmt(parse("\"Fizz\""))
                ]),
                ElseStmt([
                    IfStmt(parse("i % 5 == 0"), [
                        DisplayStmt(parse("\"Buzz\""))
                    ]),
                    ElseStmt([
                        DisplayStmt(parse("i"))
                    ])
                ])
            ]),
        ])
    ]))


def algo_sel_changed():
    current = get_current_pos()
    is_item = ui.treeWidget.currentItem() != None
    is_root = current == []
    is_editable = is_item and not is_root

    ui.btnAlgo_Add.setEnabled(is_item)
    ui.btnAlgo_Delete.setEnabled(is_editable)
    ui.btnAlgo_Edit.setEnabled(is_editable)

    can_up = is_editable and current != [0]
    ui.btnAlgo_UpBlock.setEnabled(can_up)
    ui.btnAlgo_Up.setEnabled(can_up)

    can_down = is_editable and current != [len(algo.children) - 1]
    ui.btnAlgo_Down.setEnabled(can_down)
    ui.btnAlgo_DownBlock.setEnabled(can_down)

    ui.btnAlgo_Variable.setEnabled(is_item)
    ui.btnAlgo_Display.setEnabled(is_item)
    ui.btnAlgo_Input.setEnabled(is_item)
    ui.btnAlgo_Call.setEnabled(is_item)
    ui.btnAlgo_Func.setEnabled(is_item)
    ui.btnAlgo_Return.setEnabled(is_editable)
    ui.btnAlgo_Stop.setEnabled(is_item)

    ui.btnAlgo_If.setEnabled(is_item)
    ui.btnAlgo_Else.setEnabled(is_editable)
    ui.btnAlgo_For.setEnabled(is_item)
    ui.btnAlgo_While.setEnabled(is_item)
    ui.btnAlgo_Continue.setEnabled(is_editable)
    ui.btnAlgo_Break.setEnabled(is_editable)
    ui.btnAlgo_Comment.setEnabled(is_item)

    if is_editable:
        parent, parent_stmt = get_parent(current)
        current_stmt = parent_stmt.children[current[-1]]
        ui.btnAlgo_Else.setEnabled(isinstance(current_stmt, IfStmt))

        parent_stack = [algo]
        for p in current:
            parent_stack.append(parent_stack[-1].children[p])

        in_loop = any(x for x in parent_stack if type(x) in [ForStmt, WhileStmt])
        ui.btnAlgo_Continue.setEnabled(in_loop)
        ui.btnAlgo_Break.setEnabled(in_loop)

        in_func = any(x for x in parent_stack if type(x) == FuncStmt)
        ui.btnAlgo_Return.setEnabled(in_func)


def init_ui():
    global window, ui
    window = MainWindowWrapper()
    ui = Ui_MainWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    load_code_editor()
    load_algo()

    init_action_handlers()
    refresh()

    right_corner = QMenuBar()
    ui.menubar.removeAction(ui.menuLanguage.menuAction())
    right_corner.addAction(ui.menuLanguage.menuAction())
    ui.menubar.setCornerWidget(right_corner)
    ui.btnSendInput.clicked.connect(send_user_input)
    ui.btnClearOutput.clicked.connect(clear_output)
    ui.btnPrintOutput.clicked.connect(print_output)

    ui.btnAlgo_Add.clicked.connect(btn_add_line)
    ui.btnAlgo_Delete.clicked.connect(btn_delete_line)
    ui.btnAlgo_Edit.clicked.connect(btn_edit_line)
    ui.btnAlgo_UpBlock.clicked.connect(btn_move_up_block)
    ui.btnAlgo_Up.clicked.connect(btn_move_up)
    ui.btnAlgo_Down.clicked.connect(btn_move_down)
    ui.btnAlgo_DownBlock.clicked.connect(btn_move_down_block)

    ui.btnAlgo_Variable.clicked.connect(add_def_variable)
    ui.btnAlgo_Display.clicked.connect(add_display)
    ui.btnAlgo_Input.clicked.connect(add_input)
    ui.btnAlgo_Call.clicked.connect(add_call)
    ui.btnAlgo_Func.clicked.connect(add_def_func)
    ui.btnAlgo_Return.clicked.connect(add_return)
    ui.btnAlgo_Stop.clicked.connect(add_stop_stmt)

    ui.btnAlgo_If.clicked.connect(add_if_block)
    ui.btnAlgo_Else.clicked.connect(add_else_block)
    ui.btnAlgo_For.clicked.connect(add_for_loop)
    ui.btnAlgo_While.clicked.connect(add_while_loop)
    ui.btnAlgo_Continue.clicked.connect(add_continue_stmt)
    ui.btnAlgo_Break.clicked.connect(add_break_stmt)
    ui.btnAlgo_Comment.clicked.connect(add_comment_stmt)

    ui.treeWidget.itemSelectionChanged.connect(algo_sel_changed)

    algo_sel_changed()

    def gen(act):
        return lambda: change_language(act)

    for action in ui.menuLanguage.actions():
        action.triggered.connect(gen(action.statusTip()))

    window.show()


def show_error():
    traceback.print_exc()
    # print(translate("MainWindow", "Error: ") + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2]))


def except_hook(type, value, tback):
    show_error()

    sys.__excepthook__(type, value, tback)


def setup_thread_excepthook():
    """
    Workaround for `sys.excepthook` thread bug from:
    http://bugs.python.org/issue1230540

    Call once from the main thread before creating any threads.
    """

    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):

        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            try:
                run_original(*args2, **kwargs2)
            except Exception:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


if __name__ == "__main__":
    sys.excepthook = except_hook
    setup_thread_excepthook()

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
        show_error()
        exitCode = 1

    sys.exit(exitCode)
