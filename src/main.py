# -*- coding: utf-8 -*-

import html
import os
import runpy
import sys
import tempfile
import threading
import traceback

import numpy as np
import pygments.styles
import pyqode.python.backend
from PyQt5.QtGui import *
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels

import util.code
import util.html
from algo.stmts import *
from lang import translator
from maths.nodes import *
from maths.parser import quick_parse as parse
from util import theming
from util.widgets import *

translate = QCoreApplication.translate

__version__ = "β-0.7"
__channel__ = "beta"

current_file: Optional[str] = None
can_save = False
dialog_window = None

autosave_timer = None
undo = None
mode_python = False
code_editor: api.CodeEdit = None
plot_canvas: FigureCanvas = None
plot_figure: Figure = None
plot_axes: Axes = None
panel_search = None
current_output = ""
after_output = ""
user_input: str = None
syntax_highlighter = None
algo_base_font: QFont = None
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
    ("FindNext", "FindNext"),
    ("ZoomIn", "zoom_in"),
    ("ZoomOut", "zoom_out"),
    ("ResetZoom", "reset_zoom")
]
python_only = [
    "SelectAll",
    "Find",
    "FindPrevious",
    "FindNext",
    "Replace",
    "Indent",
    "Unindent",
    "ConvertToPseudocode",
    "GoToLine"
]
algo_only = [
    "Debug",
    "Step",
    "ConvertToPython"
]
filters = {}
lng_actions = {}
app_started = False
worker = None
algo = BlockStmt([])
item_map = {}
root_item = None

block_html = '<span style="color:darkred;font-weight:bold">'
keyword_html = '<span style="color:blue;font-weight:bold">'
comment_html = '<span style="color:darkgreen;font-style:italic">'
red_html = '<span style="color:#cb4b16">'

running = False
run_started = None
skip_step = False
stopped = False
last_saved = None
current_stmt = None
python_stopped = False
settings: QSettings = None
recent_actions = None


def sleep(duration):
    begin = datetime.datetime.now()
    while (datetime.datetime.now() - begin).total_seconds() < duration:
        check_stop()
        QCoreApplication.processEvents()


def sleep_seconds(duration):
    sleep(float(duration))


def is_empty():
    if mode_python:
        return not code_editor.toPlainText()
    else:
        return algo.children == []


def is_modified():
    if mode_python:
        return code_editor.toPlainText() != last_saved
    else:
        return repr(algo) != last_saved


def add_recent(path):
    from collections import OrderedDict

    recent = settings.value("recent", [])
    recent.insert(0, path)
    recent = list(OrderedDict(zip(recent, recent)))[0:10]

    settings.setValue("recent", recent)

    update_recent_text()


def update_recent_text():
    recent = settings.value("recent", [])

    for i, file in enumerate(recent):
        recent_actions[i].setText(os.path.basename(file))
        _, ext = os.path.splitext(file.lower())

        if ext == ".alg":
            icon = QIcon(":/action/media/algobox.ico")
        elif ext == ".tr":
            icon = ui.tabWidget.tabIcon(1)
        elif ext == ".py":
            icon = ui.tabWidget.tabIcon(2)
        else:
            icon = QIcon()

        recent_actions[i].setIcon(icon)

        recent_actions[i].setVisible(True)

    for i in range(len(recent), 10):
        recent_actions[i].setVisible(False)
        recent_actions[i].setIcon(QIcon())


def recent_clicked(index):
    recent = settings.value("recent", [])

    if index < len(recent) and recent[index]:
        load_file(recent[index])


def init_recent_actions():
    global recent_actions
    recent_actions = []

    def generator(num):
        return lambda: recent_clicked(num)

    for i in range(10):
        act = QAction(window)
        act.setVisible(False)
        act.triggered.connect(generator(i))
        recent_actions.append(act)
        ui.menuRecent.insertAction(ui.actionClearRecent, act)

    ui.menuRecent.insertSeparator(ui.actionClearRecent)

    update_recent_text()


class MainWindowWrapper(QMainWindow):
    def closeEvent(self, event):
        if not is_modified():
            event.setAccepted(True)
            clean_exit()
            return
        msg = msg_box(translate("MainWindow", "Do you really want to exit?\nAll unsaved changes will be lost."),
                      parent=self)
        event.ignore()
        if msg.exec_() == QMessageBox.Yes:
            event.setAccepted(True)
            clean_exit()


def get_action(name: str) -> QAction:
    return getattr(ui, "action" + name)


def refresh():
    refresh_buttons_status()
    if not mode_python:
        refresh_algo()
        algo_sel_changed()

    if ui.tabWidget.currentIndex() == 0:
        title = "Turing"
    else:
        if current_file:
            filename = os.path.basename(current_file)
            if is_modified():
                title = translate("MainWindow", "Turing - {file} (unsaved)").format(file=filename)
            else:
                title = translate("MainWindow", "Turing - {file}").format(file=filename)
        else:
            title = translate("MainWindow", "Turing - New File")

    window.setWindowTitle(title)


def refresh_buttons_status():
    if mode_python:
        for ours, theirs in editor_action_table:
            get_action(ours).setEnabled(getattr(code_editor, "action_" + theirs).isEnabled())

    active_code = True
    for c in [
        "Save",
        "SaveAs",
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

    for c in algo_only:
        get_action(c).setVisible(not mode_python)

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
    else:
        btn_dupl_line()


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
    calculator.CalculatorWindow()


def handler_HelpContents():
    from forms import help
    help.HelpWindow(window)


def change_tab():
    global mode_python
    if ui.tabWidget.currentIndex() == 1:
        mode_python = False
    elif ui.tabWidget.currentIndex() == 2:
        mode_python = True
    refresh()


def python_print(*args, end="\n"):
    global current_output
    current_output += html.escape(" ".join(str(arg) for arg in args))
    current_output += end
    update_output()


def update_output():
    global current_output
    ui.txtOutput.setHtml('<pre style="margin: 0">%s</pre>' % (current_output + after_output))
    ui.txtOutput.moveCursor(QTextCursor.End)
    ui.txtOutput.ensureCursorVisible()
    if current_output.endswith("\n\n"):
        current_output = current_output[:-1]


def check_stop():
    if stopped or (not mode_python and worker.finished):
        raise KeyboardInterrupt()


def python_input(prompt="", globals=None, locals=None):
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
        sleep(0.050)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
        sleep(0.050)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff5252; }")
        sleep(0.050)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
        sleep(0.050)
        ui.txtInput.setStyleSheet("QLineEdit { background-color: #ffbaba; }")
        sleep(0.050)
        ui.txtInput.setStyleSheet("")
        sleep(0.200)

    global user_input
    user_input = None

    ui.txtInput.setFocus(Qt.OtherFocusReason)

    while user_input is None:
        check_stop()
        QCoreApplication.processEvents()

    ui.btnSendInput.setEnabled(False)
    ui.txtInput.setEnabled(False)
    ui.txtInput.setText("")

    after_output = ""
    python_print(user_input)
    update_output()

    try:
        evaled = eval(user_input, globals, locals)
        return evaled
    except:
        try:
            to_int = int(user_input)
            return to_int
        except:
            try:
                to_float = float(user_input)
                return to_float
            except:
                try:
                    to_complex = complex(user_input)
                    return to_complex
                except:
                    return user_input


def python_print_error(msg, end="\n"):
    global current_output
    current_output += util.html.color_span(msg, "red") + end
    if not mode_python:
        set_current_line(worker.last, True)
    update_output()


def update_plot():
    plot_axes.grid(linestyle='-')
    plot_canvas.draw()


def g_clear():
    plot_axes.clear()
    plot_axes.axhline(y=0, color='k')
    plot_axes.axvline(x=0, color='k')
    g_window(-10, 10, -10, 10)


def g_window(xmin, xmax, ymin, ymax, xgrad=1, ygrad=1):
    plot_axes.set_xlim(xmin, xmax)
    plot_axes.set_ylim(ymin, ymax)
    # plot_axes.set_xticks(range(xmin, xmax, xgrad))
    # plot_axes.set_yticks(range(ymin, ymax, ygrad))
    update_plot()


def g_point(x, y, color="red"):
    plot_axes.scatter([x], [y], c=color)
    update_plot()


def g_line(startx, starty, endx, endy, color="red"):
    plot_axes.plot([startx, endx], [starty, endy], c=color, linestyle="-", marker="o")
    update_plot()


def g_func(func, start, end, step, color="red"):
    domain = np.arange(start, end, step)
    results = [func(x) for x in domain]
    plot_axes.plot(domain, results, c=color, linestyle="-")
    update_plot()


def stmt_GClear(stmt: GClearStmt):
    g_clear()


def stmt_GWindow(stmt: GWindowStmt):
    g_window(worker.evaluator.eval_node(stmt.x_min),
             worker.evaluator.eval_node(stmt.x_max),
             worker.evaluator.eval_node(stmt.y_min),
             worker.evaluator.eval_node(stmt.y_max),
             worker.evaluator.eval_node(stmt.x_grad),
             worker.evaluator.eval_node(stmt.y_grad))


def stmt_GPoint(stmt: GPointStmt):
    g_point(worker.evaluator.eval_node(stmt.x), worker.evaluator.eval_node(stmt.y),
            worker.evaluator.eval_node(stmt.color))


def stmt_GLine(stmt: GLineStmt):
    g_line(worker.evaluator.eval_node(stmt.start_x),
           worker.evaluator.eval_node(stmt.start_y),
           worker.evaluator.eval_node(stmt.end_x),
           worker.evaluator.eval_node(stmt.end_y),
           worker.evaluator.eval_node(stmt.color))


def stmt_GFunc(stmt: GFuncStmt):
    g_func(worker.evaluator.eval_node(stmt.get_function()),
           worker.evaluator.eval_node(stmt.start),
           worker.evaluator.eval_node(stmt.end),
           worker.evaluator.eval_node(stmt.step),
           worker.evaluator.eval_node(stmt.color))


def stmt_Sleep(stmt: SleepStmt):
    sleep_seconds(worker.evaluator.eval_node(stmt.duration))


def init_worker():
    from algo.worker import Worker
    global worker
    worker = Worker(algo.children)
    worker.callback_print = python_print
    worker.callback_input = python_input
    worker.log.set_callback(python_print_error)
    worker.log.use_prefix = False
    worker.init()
    worker.callback_stop = callback_stop
    worker.map[GClearStmt] = stmt_GClear
    worker.map[GWindowStmt] = stmt_GWindow
    worker.map[GPointStmt] = stmt_GPoint
    worker.map[GLineStmt] = stmt_GLine
    worker.map[GFuncStmt] = stmt_GFunc
    worker.map[SleepStmt] = stmt_Sleep
    set_current_line(None)
    g_clear()


def end_output():
    global current_output, run_started
    current_output += util.html.centered(
        util.html.color_span(translate("MainWindow", "end of output") if run_started is None
                             else translate("MainWindow", "end of output [{time}]").format(
            time=datetime.datetime.now() - run_started), "red"))
    current_output += "<hr />\n"
    run_started = None
    update_output()


def set_current_line(current: Optional[BaseStmt], error=False):
    for item, stmt in item_map.values():
        if stmt == current:
            item.setBackground(0, QBrush(QColor("#ef5350") if error else QColor("#fdd835")))
        else:
            item.setBackground(0, root_item.background(0))


def callback_stop(stmt, virtual=False):
    breakpoint_message(worker.evaluator.eval_node(stmt.message))
    if not virtual:
        worker.finished = True


def breakpoint_message(message=""):
    global after_output
    after_output = "<hr>"
    after_output += util.html.centered(
        "<h3>%s</h3>" % util.html.color_span("<i>%s</i>" % (
            translate("MainWindow", "Breakpoint: ") + html.escape(str(message)) if message else translate("MainWindow",
                                                                                                     "Breakpoint")),
                                             "red"))
    update_output()


def python_breakpoint(message=""):
    global after_output
    breakpoint_message(message)

    global python_stopped
    python_stopped = True

    ui.actionRun.setDisabled(False)
    ui.actionStop.setDisabled(False)

    while python_stopped and not stopped:
        QCoreApplication.processEvents()

    if stopped:
        raise KeyboardInterrupt()

    after_output = ""
    update_output()

    ui.actionRun.setDisabled(True)
    ui.actionStop.setDisabled(True)


def handler_Stop():
    python_print_error(translate("MainWindow", "program interrupted"))
    global running, after_output, stopped
    after_output = ""
    stopped = True
    if mode_python:
        running = False
    else:
        running = True
        worker.finished = True
        worker.error = False
        handler_Step()
    update_output()


def handler_Step():
    ui.actionRun.setDisabled(True)
    ui.actionDebug.setDisabled(True)
    ui.actionStep.setDisabled(True)
    ui.actionStop.setEnabled(True)
    global running, current_stmt, skip_step, stopped

    try:
        if mode_python:
            pass
        else:
            if not stopped:
                if running:
                    if skip_step:
                        skip_step = False
                        global after_output
                        after_output = ""
                        update_output()
                    else:
                        if isinstance(current_stmt, StopStmt):
                            callback_stop(current_stmt, True)
                            skip_step = True
                        else:
                            worker.exec_stmt(current_stmt)
                else:
                    init_worker()
                    running = True

                if not skip_step and not worker.error:
                    current_stmt = worker.next_stmt()

                    set_current_line(current_stmt)
            else:
                stopped = False
    except:
        show_error()
    finally:
        if worker.finished:
            ui.actionRun.setDisabled(False)
            end_output()
            if not worker.error:
                set_current_line(None)
            running = False
        ui.actionDebug.setDisabled(False)
        ui.actionStep.setDisabled(False)
        ui.actionStop.setEnabled(not worker.finished)


def handler_Debug():
    handler_Run(True)


class compat_list(list):
    def __init__(self, iterable=()):
        super().__init__(iterable)

    def __setitem__(self, key, value):
        while len(self) <= key:
            self.append(0)

        super().__setitem__(key, value)


def handler_Run(flag=False):
    global python_stopped
    if python_stopped:
        python_stopped = False
        return

    if not flag and not mode_python:
        algo_run_python()
        return

    ui.actionRun.setDisabled(True)
    ui.actionDebug.setDisabled(True)
    ui.actionStep.setDisabled(True)
    ui.actionStop.setEnabled(True)
    global running, current_stmt, skip_step, stopped, run_started
    user_stop = False
    set_current_line(None)
    try:
        if mode_python:
            file = tempfile.NamedTemporaryFile(mode="w+b", suffix=".py", delete=False)
            try:
                code = util.code.python_wrapper(code_editor.toPlainText()).encode("utf8")
                file.write(code)
                file.close()
                running = True
                stopped = False
                python_stopped = False
                g_clear()
                run_started = datetime.datetime.now()
                runpy.run_path(file.name, init_globals={
                    "print": python_print,
                    "input": python_input,
                    "breakpoint": python_breakpoint,
                    "list": compat_list,
                    "sleep": sleep_seconds,

                    "g_clear": g_clear,
                    "g_window": g_window,
                    "g_point": g_point,
                    "g_line": g_line,
                    "g_func": g_func
                })
            except SyntaxError as err:
                msg = translate("MainWindow", "Syntax error ({type}) at line {line}, offset {off}: ").format(
                    type=type(err).__name__, line=err.lineno - 10, off=err.offset)
                python_print_error(msg + html.escape(err.text), end="")
                python_print_error(" " * (len(msg) + err.offset - 1) + "↑")
            except KeyboardInterrupt:
                pass
            except:
                python_print_error(html.escape(str(sys.exc_info()[1])))
            finally:
                os.unlink(file.name)
        else:
            if not running:
                init_worker()
                g_clear()
                worker.break_on_error = True
                running = True
                stopped = False
                run_started = datetime.datetime.now()
                skip_step = False
            else:
                if skip_step:
                    skip_step = False
                    global after_output
                    after_output = ""
                    update_output()
                else:
                    worker.exec_stmt(current_stmt)
                    if not worker.error:
                        set_current_line(None)

            while not worker.finished:
                worker.step()
    except KeyboardInterrupt:
        user_stop = True
    except:
        show_error()
    finally:
        if not mode_python and worker.stopped:
            ui.actionStep.setDisabled(False)
            ui.actionDebug.setDisabled(False)
            set_current_line(worker.last)
            skip_step = True
            worker.finished = False
            worker.stopped = False
        else:
            if not user_stop:
                end_output()
            ui.actionRun.setDisabled(False)
            ui.actionStep.setDisabled(False)
            ui.actionDebug.setDisabled(False)
            ui.actionStop.setEnabled(False)
            running = False


def handler_ConvertToPython():
    global mode_python, current_file
    py_code = "\n".join(algo.python())
    code_editor.setPlainText(py_code, "", "")
    mode_python = True
    current_file = None
    refresh()


def algo_run_python():
    global mode_python
    py_code = "\n".join(algo.python())
    code_editor.setPlainText(py_code, "", "")
    mode_python = True
    handler_Run()
    mode_python = False
    # code_editor.setPlainText("", "", "")


def handler_AboutTuring():
    import forms.about
    forms.about.AboutWindow(window, __version__, __channel__).run()


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


def save(filename):
    global last_saved

    if mode_python:
        last_saved = str(code_editor.toPlainText())
    else:
        last_saved = repr(algo)

    with open(filename, "w+", encoding="utf8") as savefile:
        savefile.write(last_saved)

    add_recent(filename)

    refresh()


def save_output():
    file = QFileDialog.getSaveFileName(window, translate("MainWindow", "Save output"),
                                       "",
                                       translate("MainWindow", "Text files (*.txt)"))[0]
    if not file:
        return

    with open(file, "w+", encoding="utf8") as savefile:
        savefile.write(ui.txtOutput.toPlainText())


def handler_SaveAs():
    global current_file

    file = QFileDialog.getSaveFileName(window, translate("MainWindow", "Save"),
                                       "",
                                       filters[["tr", "py"][mode_python]])[0]
    if not file:
        return

    current_file = file
    handler_Save()


def handler_Save():
    if not current_file:
        handler_SaveAs()
        return

    save(current_file)


def handler_Open():
    global algo, current_file
    sel_file, _ = QFileDialog.getOpenFileName(window, translate("MainWindow", "Open"), "", ";;".join(filters.values()))

    if not sel_file:
        return

    load_file(sel_file)


def load_file(file):
    global current_file, mode_python, last_saved
    current_file = file
    _, ext = os.path.splitext(current_file.lower())

    with open(current_file, "r", encoding="utf8") as openfile:
        newcode = openfile.read()

    if ext == ".alg":
        from algo.algobox import parse_algobox
        mode_python = False
        load_block(parse_algobox(newcode))
        last_saved = repr(algo)

    elif ext == ".tr":
        mode_python = False
        load_pseudocode(newcode)
        last_saved = repr(algo)

    elif ext == ".py":
        mode_python = True
        code_editor.setPlainText(newcode, "", "")
        last_saved = newcode

    add_recent(current_file)

    refresh()


def handler_New():
    if is_modified():
        msg = msg_box(translate("MainWindow", "Do you really want to create a new file?\nAll unsaved changes will be lost."),
                      parent=window)
        if msg.exec_() != QMessageBox.Yes:
            return

    global current_file, algo, code_editor
    current_file = None
    algo = BlockStmt([])
    code_editor.setPlainText("", "", "")
    refresh()


def handler_ZoomIn():
    if mode_python:
        code_editor.zoom_in()
    else:
        set_algo_size(ui.treeWidget.font().pointSize() + 1)


def handler_ZoomOut():
    if mode_python:
        code_editor.zoom_out()
    else:
        set_algo_size(ui.treeWidget.font().pointSize() - 1)


def handler_ResetZoom():
    if mode_python:
        code_editor.reset_zoom()
    else:
        set_algo_size(algo_base_font.pointSize())


def set_algo_size(size):
    if size < 1:
        size = 1
    set_font_size(ui.treeWidget, size)
    for idstmt, (item, stmt) in item_map.items():
        set_font_size(item, size, 0)
        if hasattr(item, "lbl"):
            set_font_size(item.lbl, size)


def init_action_handlers():
    for item in dir(ui):
        if item.startswith("action"):
            name = "handler_" + item[6:]

            if name in globals():
                getattr(ui, item).triggered.connect(globals()[name])


def copy_action(source: QAction, target: QAction):
    target.setText(source.text())
    target.setIcon(source.icon())
    target.triggered.disconnect()
    target.triggered.connect(source.trigger)


def load_languages():
    def gen(loc):
        return lambda: change_language(loc)

    it = QDirIterator(":/lang/media/lang")

    while it.hasNext():
        cur = it.next()
        locale_name, _ = os.path.splitext(os.path.basename(cur))
        locale = QLocale(locale_name)
        act = QAction(window)
        act.setCheckable(True)
        act.setIcon(QIcon(cur))
        act.setText(locale.nativeLanguageName())
        act.triggered.connect(gen(locale_name))
        ui.menuLanguage.addAction(act)
        lng_actions[locale_name] = act


def fix_tabwidget_width():
    ui.tabWidget_2.setMinimumWidth(
        sum(ui.tabWidget_2.tabBar().tabSizeHint(x).width() for x in range(ui.tabWidget_2.count())))
    ui.widget.setMinimumWidth(0)
    ui.widget.setMaximumWidth(16777215)
    ui.widget.adjustSize()
    width = max(window.width() / 3, ui.widget.width())
    ui.widget.setMinimumWidth(width)
    ui.widget.setMaximumWidth(width)


def change_language(language: str):
    available = lng_actions.keys()
    if language not in available and util.get_short_lang(language) not in available:
        language = "en"
    translator.load(language)
    ui.menubar.resizeEvent(QResizeEvent(ui.menubar.size(), ui.menubar.size()))
    load_editor_actions()
    for l, a in lng_actions.items():
        a.setChecked(l in [language, util.get_short_lang(language)])
    fix_qt_shitty_margins()
    fix_tabwidget_width()
    refresh()


def send_user_input():
    global user_input
    user_input = ui.txtInput.text()


def clear_output():
    global current_output
    current_output = ""
    if not mode_python:
        set_current_line(None)
    update_output()
    g_clear()


def print_output():
    print(dir(code_editor))

    theming.themes["devtest"] = (theming.themes["devtest"][0], code_editor.toPlainText().split("\n"))
    set_theme("devtest")

    pass


def load_editor_actions():
    for ours, theirs in editor_action_table:
        copy_action(getattr(ui, "action" + ours), getattr(code_editor, "action_" + theirs))

    # edge cases
    copy_action(ui.actionFind, panel_search.menu.menuAction())
    code_editor._sub_menus["Advanced"].setTitle(translate("MainWindow", "Advanced"))
    mode_zoom.mnu_zoom.setTitle(translate("MainWindow", "Zoom"))

    panel_folding.context_menu.setTitle(translate("MainWindow", "Folding"))
    panel_folding.context_menu.actions()[0].setText(translate("MainWindow", "Collapse"))
    panel_folding.context_menu.actions()[1].setText(translate("MainWindow", "Expand"))
    panel_folding.context_menu.actions()[3].setText(translate("MainWindow", "Collapse all"))
    panel_folding.context_menu.actions()[4].setText(translate("MainWindow", "Expand all"))

    mode_ext_select.action_select_word.setText(translate("MainWindow", "Select word"))
    mode_ext_select.action_select_extended_word.setText(translate("MainWindow", "Select extended word"))
    mode_ext_select.action_select_matched.setText(translate("MainWindow", "Matched select"))
    mode_ext_select.action_select_line.setText(translate("MainWindow", "Select line"))
    mode_ext_select.action_select_line.associatedWidgets()[0].setTitle(translate("MainWindow", "Select"))

    panel_search.labelSearch.setPixmap(ui.actionFind.icon().pixmap(16, 16))
    panel_search.labelSearch.setMaximumSize(QSize(16, 16))
    panel_search.labelReplace.setPixmap(ui.actionReplace.icon().pixmap(16, 16))
    panel_search.labelReplace.setMaximumSize(QSize(16, 16))
    panel_search.toolButtonPrevious.setIcon(QIcon(QPixmap(":/action/media/up.png")))
    panel_search.toolButtonNext.setIcon(QIcon(QPixmap(":/action/media/down.png")))
    panel_search.toolButtonClose.setIcon(QIcon(QPixmap(":/action/media/cross.png")))

    panel_search.checkBoxRegex.setText(translate("MainWindow", "Regex"))
    panel_search.checkBoxCase.setText(translate("MainWindow", "Match case"))
    panel_search.checkBoxWholeWords.setText(translate("MainWindow", "Whole words"))
    panel_search.checkBoxInSelection.setText(translate("MainWindow", "In Selection"))
    panel_search.labelMatches.setText(translate("MainWindow", "0 matches"))
    panel_search.toolButtonReplace.setText(translate("MainWindow", "Replace"))
    panel_search.toolButtonReplaceAll.setText(translate("MainWindow", "Replace All"))
    panel_search.lineEditSearch.prompt_text = translate("MainWindow", "Find")
    panel_search.lineEditSearch.button.setIcon(QIcon(QPixmap(":/action/media/backspace.png")))
    panel_search.lineEditSearch.button.setMinimumSize(QSize(21, 21))
    panel_search.lineEditReplace.prompt_text = translate("MainWindow", "Replace")
    panel_search.lineEditReplace.button.setIcon(QIcon(QPixmap(":/action/media/backspace.png")))


def copy_actions_to_editor(panel):
    for name, obj in panel.__dict__.items():
        if name.startswith("action_"):
            setattr(code_editor, name, obj)
        elif name.startswith("action"):  # workaround for shitty naming by the devs
            setattr(code_editor, "action_" + name[6:], obj)


def set_theme(theme):
    settings.setValue("app_theme", theme)
    theming.load_theme(theme)

    for act in ui.menuChangeTheme.actions():
        act.setChecked(act.statusTip() == theme)


def set_style(style):
    settings.setValue("editor_style", style)
    syntax_highlighter.pygments_style = style

    for act in ui.menuChangeStyle.actions():
        act.setChecked(act.text() == style)


def load_code_editor():
    global code_editor
    code_editor = api.CodeEdit()
    if hasattr(sys, "frozen"):
        print("using external backend")
        if sys.platform == "win32":
            backend = "editor_backend.exe"
        elif sys.platform == "linux":
            backend = "editor_backend"
        elif sys.platform == "darwin":
            backend = "editor_backend"
    else:
        print("using script file")
        import editor_backend
        backend = editor_backend.__file__
    code_editor.backend.start(backend)

    code_editor.modes.append(modes.CodeCompletionMode())
    code_editor.modes.append(modes.CaretLineHighlighterMode())
    code_editor.modes.append(modes.AutoCompleteMode())
    code_editor.modes.append(modes.IndenterMode())
    code_editor.modes.append(modes.AutoIndentMode())
    code_editor.modes.append(modes.OccurrencesHighlighterMode())
    code_editor.modes.append(modes.SmartBackSpaceMode())
    code_editor.modes.append(modes.SymbolMatcherMode())
    global mode_zoom
    mode_zoom = modes.ZoomMode()
    code_editor.modes.append(mode_zoom)
    code_editor.action_zoom_in = mode_zoom.mnu_zoom.actions()[0]
    code_editor.action_zoom_out = mode_zoom.mnu_zoom.actions()[1]
    code_editor.action_reset_zoom = mode_zoom.mnu_zoom.actions()[2]

    global mode_ext_select
    mode_ext_select = code_editor.modes.append(modes.ExtendedSelectionMode())

    global syntax_highlighter
    syntax_highlighter = code_editor.modes.append(modes.PygmentsSyntaxHighlighter(code_editor.document()))
    syntax_highlighter.fold_detector = api.IndentFoldDetector()

    global panel_folding
    panel_folding = code_editor.panels.append(panels.FoldingPanel())
    code_editor.panels.append(panels.LineNumberPanel())
    code_editor.modes.append(modes.CheckerMode(pyqode.python.backend.run_pep8))
    code_editor.panels.append(panels.GlobalCheckerPanel(), panels.GlobalCheckerPanel.Position.LEFT)
    global panel_search
    panel_search = code_editor.panels.append(panels.SearchAndReplacePanel(), api.Panel.Position.BOTTOM)

    panel_search._update_label_matches_orig = panel_search._update_label_matches

    def wrapper():
        panel_search._update_label_matches_orig()
        if panel_search.labelMatches.text():
            panel_search.labelMatches.setText(
                translate("MainWindow", "{num} matches").format(num=panel_search.cpt_occurences))

    panel_search._update_label_matches = wrapper

    copy_actions_to_editor(panel_search)

    code_editor.textChanged.connect(refresh)

    load_editor_actions()

    def gen(s):
        return lambda: set_style(s)

    for style in pygments.styles.get_all_styles():
        action = QAction(window)
        action.setText(style)
        action.setCheckable(True)
        action.triggered.connect(gen(style))
        ui.menuChangeStyle.addAction(action)

    syntax_highlighter.pygments_style = settings.value("editor_style", "default")
    set_style(syntax_highlighter.pygments_style)

    ui.verticalLayout_8.addWidget(code_editor)


def load_plot_canvas():
    global plot_canvas, plot_figure, plot_axes
    plot_figure = Figure()
    plot_axes = plot_figure.add_subplot(111)
    plot_canvas = FigureCanvas(plot_figure)
    g_clear()
    g_window(-10, 10, -10, 10)
    ui.verticalLayout_4.addWidget(plot_canvas)


def get_item_label(item):
    def gen_func(item):
        return lambda: ui.treeWidget.setCurrentItem(item)

    txt = QClickableLabel()
    txt.setStyleSheet(ui.treeWidget.styleSheet())
    txt.clicked.connect(gen_func(item))
    txt.dclicked.connect(algo_double_click)
    item.lbl = txt
    ui.treeWidget.setItemWidget(item, 0, txt)
    ui.treeWidget.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    return txt


def get_item_html(html, data=""):
    item = QTreeWidgetItem()
    item.setStatusTip(0, data)
    item.setFont(0, ui.treeWidget.font())
    lbl = get_item_label(item)
    lbl.setFont(item.font(0))
    lbl.setText('&nbsp;<span>%s</span>' % html)

    ui.treeWidget.setItemWidget(item, 0, lbl)

    return item, lbl


def refresh_algo_text():
    for item, stmt in item_map.values():
        lbl = get_item_label(item)
        lbl.setText('&nbsp;<span>%s</span>' % str_stmt(stmt))


def add_display():
    from forms import alg_display
    dlg = alg_display.AlgoDisplayStmt(window)
    if dlg.run():
        append_line(DisplayStmt(dlg.expr, dlg.newline))


def add_def_variable():
    from forms import alg_define
    dlg = alg_define.AlgoDefineStmt(window)
    if dlg.run():
        append_line(AssignStmt(dlg.varname, dlg.expr))


def add_input():
    from forms import alg_input
    dlg = alg_input.AlgoInputStmt(window)
    if dlg.run():
        append_line(InputStmt(dlg.varname, dlg.expr))


def add_call():
    from forms import alg_call
    dlg = alg_call.AlgoCallStmt(window)
    if dlg.run():
        append_line(CallStmt(dlg.func, dlg.args))


def add_def_func():
    from forms import alg_func
    dlg = alg_func.AlgoFuncStmt(window)
    if dlg.run():
        append_line(FuncStmt(dlg.func, dlg.args, []))


def add_return():
    from forms import alg_return
    dlg = alg_return.AlgoReturnStmt(window)
    if dlg.run():
        append_line(ReturnStmt(dlg.expr))


def add_if_block():
    from forms import alg_if
    dlg = alg_if.AlgoIfStmt(window)
    if dlg.run():
        append_line(IfStmt(dlg.expr, []))


def add_else_block():
    append_line(ElseStmt([]))


def add_for_loop():
    from forms import alg_for
    dlg = alg_for.AlgoForStmt(window)
    if dlg.run():
        append_line(ForStmt(dlg.varname, dlg.f_from, dlg.f_to, [], dlg.f_step))


def add_while_loop():
    from forms import alg_while
    dlg = alg_while.AlgoWhileStmt(window)
    if dlg.run():
        append_line(WhileStmt(dlg.expr, []))


def add_gclear():
    append_line(GClearStmt())


def add_gline():
    from forms import alg_gline
    dlg = alg_gline.AlgoGLineStmt(window)
    if dlg.run():
        append_line(GLineStmt(dlg.f_start_x, dlg.f_start_y, dlg.f_end_x, dlg.f_end_y, dlg.f_color))


def add_gpoint():
    from forms import alg_gpoint
    dlg = alg_gpoint.AlgoGPointStmt(window)
    if dlg.run():
        append_line(GPointStmt(dlg.f_x, dlg.f_y, dlg.f_color))


def add_gwindow():
    from forms import alg_gwindow
    dlg = alg_gwindow.AlgoGWindowStmt(window)
    if dlg.run():
        append_line(GWindowStmt(dlg.f_x_min, dlg.f_x_max, dlg.f_y_min, dlg.f_y_max, dlg.f_x_grad, dlg.f_y_grad))


def add_gfunc():
    from forms import alg_gfunc
    dlg = alg_gfunc.AlgoGFuncStmt(window)
    if dlg.run():
        append_line(GFuncStmt(dlg.f_variable, dlg.f_function, dlg.f_start, dlg.f_end, dlg.f_step, dlg.f_color))


def add_break_stmt():
    append_line(BreakStmt())


def add_continue_stmt():
    append_line(ContinueStmt())


def add_stop_stmt():
    from forms import alg_stop
    dlg = alg_stop.AlgoStopStmt(window)
    if dlg.run():
        append_line(StopStmt(dlg.expr))


def add_sleep_stmt():
    from forms import alg_sleep
    dlg = alg_sleep.AlgoSleepStmt(window)
    if dlg.run():
        append_line(SleepStmt(dlg.expr))


def add_comment_stmt():
    from forms import alg_comment
    dlg = alg_comment.AlgoCommentStmt(window)
    if dlg.run():
        append_line(CommentStmt(dlg.comment))


def btn_dupl_line():
    stmt = get_current_stmt()

    if isinstance(stmt, IfStmt):
        current_pos = get_current_pos()
        _, parent_stmt = get_parent(current_pos)
        if current_pos[-1] + 1 < len(parent_stmt.children) and isinstance(parent_stmt.children[current_pos[-1] + 1],
                                                                          ElseStmt):
            append_line(eval(repr(parent_stmt.children[current_pos[-1] + 1])), True)

    append_line(eval(repr(stmt)), True)


def btn_delete_line():
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)

    if isinstance(parent_stmt.children[current_pos[-1]], IfStmt) and current_pos[-1] < len(
            parent_stmt.children) - 1 and isinstance(parent_stmt.children[current_pos[-1] + 1], ElseStmt):
        del parent_stmt.children[current_pos[-1] + 1]

    del parent_stmt.children[current_pos[-1]]

    refresh()


def btn_edit_line():
    stmt = get_current_stmt()

    if isinstance(stmt, DisplayStmt):
        from forms import alg_display
        dlg = alg_display.AlgoDisplayStmt(window, (stmt.content.code(), stmt.newline))
        if dlg.run():
            stmt.content = dlg.expr
            stmt.newline = dlg.newline

    elif isinstance(stmt, CallStmt):
        from forms import alg_call
        dlg = alg_call.AlgoCallStmt(window, (stmt.function.code(), [x.code() for x in stmt.arguments]))
        if dlg.run():
            stmt.function = dlg.func
            stmt.arguments = dlg.args

    elif isinstance(stmt, AssignStmt):
        from forms import alg_define
        dlg = alg_define.AlgoDefineStmt(window, (stmt.variable.code(), stmt.value.code()))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.value = dlg.expr

    elif isinstance(stmt, ReturnStmt):
        from forms import alg_return
        dlg = alg_return.AlgoReturnStmt(window, stmt.value.code() if stmt.value is not None else None)
        if dlg.run():
            stmt.value = dlg.expr

    elif isinstance(stmt, StopStmt):
        from forms import alg_stop
        dlg = alg_stop.AlgoStopStmt(window, stmt.message.code() if stmt.message is not None else None)
        if dlg.run():
            stmt.message = dlg.expr

    elif isinstance(stmt, SleepStmt):
        from forms import alg_sleep
        dlg = alg_sleep.AlgoSleepStmt(window, stmt.duration.code())
        if dlg.run():
            stmt.duration = dlg.expr

    elif isinstance(stmt, InputStmt):
        from forms import alg_input
        dlg = alg_input.AlgoInputStmt(window,
                                      (stmt.variable.code(), stmt.prompt.code() if stmt.prompt is not None else None))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.prompt = dlg.expr

    elif isinstance(stmt, IfStmt):
        from forms import alg_if
        dlg = alg_if.AlgoIfStmt(window, stmt.condition.code())
        if dlg.run():
            stmt.condition = dlg.expr

    elif isinstance(stmt, WhileStmt):
        from forms import alg_while
        dlg = alg_while.AlgoWhileStmt(window, stmt.condition.code())
        if dlg.run():
            stmt.condition = dlg.expr

    elif isinstance(stmt, ForStmt):
        from forms import alg_for
        dlg = alg_for.AlgoForStmt(window, (
            stmt.variable, stmt.begin.code(), stmt.end.code(), stmt.step.code() if stmt.step is not None else None))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.begin = dlg.f_from
            stmt.end = dlg.f_to
            stmt.step = dlg.f_step

    elif isinstance(stmt, FuncStmt):
        from forms import alg_func
        dlg = alg_func.AlgoFuncStmt(window, (stmt.name, stmt.parameters))
        if dlg.run():
            stmt.name = dlg.func
            stmt.parameters = dlg.args

    elif isinstance(stmt, CommentStmt):
        from forms import alg_comment
        dlg = alg_comment.AlgoCommentStmt(window, stmt.content)
        if dlg.run():
            stmt.content = dlg.comment

    elif isinstance(stmt, GLineStmt):
        from forms import alg_gline
        dlg = alg_gline.AlgoGLineStmt(window, (
            stmt.start_x.code(), stmt.start_y.code(), stmt.end_x.code(), stmt.end_y.code(), stmt.color.code()))
        if dlg.run():
            stmt.start_x = dlg.f_start_x
            stmt.start_y = dlg.f_start_y
            stmt.end_x = dlg.f_end_x
            stmt.end_y = dlg.f_end_y
            stmt.color = dlg.f_color

    elif isinstance(stmt, GPointStmt):
        from forms import alg_gpoint
        dlg = alg_gpoint.AlgoGPointStmt(window, (stmt.x.code(), stmt.y.code(), stmt.color.code()))
        if dlg.run():
            stmt.x = dlg.f_x
            stmt.y = dlg.f_y
            stmt.color = dlg.f_color

    elif isinstance(stmt, GWindowStmt):
        from forms import alg_gwindow
        dlg = alg_gwindow.AlgoGWindowStmt(window, (
            stmt.x_min.code(), stmt.x_max.code(), stmt.y_min.code(), stmt.y_max.code(), stmt.x_grad.code(),
            stmt.y_grad.code()))
        if dlg.run():
            stmt.x_min = dlg.f_x_min
            stmt.x_max = dlg.f_x_max
            stmt.y_min = dlg.f_y_min
            stmt.y_max = dlg.f_y_max
            stmt.x_grad = dlg.f_x_grad
            stmt.y_grad = dlg.f_y_grad

    elif isinstance(stmt, GFuncStmt):
        from forms import alg_gfunc
        dlg = alg_gfunc.AlgoGFuncStmt(window, (
        stmt.var, stmt.expr.code(), stmt.start.code(), stmt.end.code(), stmt.step.code(), stmt.color.code()))
        if dlg.run():
            stmt.var = dlg.f_variable
            stmt.expr = dlg.f_function
            stmt.start = dlg.f_start
            stmt.end = dlg.f_end
            stmt.step = dlg.f_step
            stmt.color = dlg.f_color

    refresh()


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


def append_line(stmt, force_after=False):
    current_pos = get_current_pos()
    _, parent_stmt = get_parent(current_pos)
    if current_pos:
        existing = parent_stmt.children[current_pos[-1]]
        if type(existing) == BaseStmt:
            parent_stmt.children[current_pos[-1]] = stmt
            refresh()
            return
    else:
        existing = algo

    if force_after and isinstance(existing, IfStmt) and current_pos[-1] + 1 < len(parent_stmt.children) and isinstance(
            parent_stmt.children[current_pos[-1] + 1], ElseStmt):
        current_pos[-1] += 1

    if not force_after and isinstance(existing, BlockStmt) \
            and not (isinstance(stmt, ElseStmt) and isinstance(existing, IfStmt)):
        current_pos.append(len(existing.children))
    else:
        current_pos[-1] += 1

    add_line(current_pos, stmt)

    if isinstance(stmt, BlockStmt):
        add_block(stmt, current_pos)

    set_current_stmt(stmt)


def get_current_stmt():
    current_item = ui.treeWidget.currentItem()

    if current_item is not None:
        for item, stmt in item_map.values():
            if item == current_item:
                return stmt

    return algo


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


def set_current_stmt(current):
    if current is None:
        return

    for item, stmt in item_map.values():
        if stmt == current:
            ui.treeWidget.setCurrentItem(item)
            break


def refresh_algo():
    current = None
    line = ui.treeWidget.currentItem()
    for item, stmt in item_map.values():
        if item == line:
            current = stmt
            break

    load_block(algo)

    set_current_stmt(current)


def move_line(old_pos, new_pos):
    _, old_parent_stmt = get_parent(old_pos)
    _, new_parent_stmt = get_parent(new_pos)

    line = old_parent_stmt.children[old_pos[-1]]
    del old_parent_stmt.children[old_pos[-1]]
    new_parent_stmt.children.insert(new_pos[-1], line)

    refresh()


def add_line(pos, stmt, add=True):
    parent, parent_stmt = get_parent(pos)

    item, lbl = get_item_html(str_stmt(stmt))

    parent.insertChild(pos[-1], item)
    if add:
        parent_stmt.children.insert(pos[-1], stmt)

    store_line(item, stmt)

    ui.treeWidget.setItemWidget(item, 0, lbl)


def str_stmt(stmt):
    code = lambda stmt: stmt.code(True)

    if isinstance(stmt, DisplayStmt):
        ret = translate("Algo", "[k]DISPLAY[/k] [c]{val}[/c]").format(val=code(stmt.content))

    elif isinstance(stmt, BreakStmt):
        ret = translate("Algo", "[k]BREAK[/k]")

    elif isinstance(stmt, ContinueStmt):
        ret = translate("Algo", "[k]CONTINUE[/k]")

    elif isinstance(stmt, ElseStmt):
        ret = translate("Algo", "[b]ELSE[/b]")

    elif isinstance(stmt, WhileStmt):
        ret = translate("Algo", "[b]WHILE[/b] [c]{cond}[/c]").format(cond=code(stmt.condition))

    elif isinstance(stmt, IfStmt):
        ret = translate("Algo", "[b]IF[/b] [c]{cond}[/c]").format(cond=code(stmt.condition))

    elif isinstance(stmt, InputStmt):
        ret = translate("Algo", "[k]INPUT[/k] [c]{prompt}[/c] [k]TO[/k] [c]{var}[/c]").format(
            prompt="" if stmt.prompt is None else stmt.prompt.code(True), var=code(stmt.variable))

    elif isinstance(stmt, AssignStmt):
        if stmt.value is None:
            ret = translate("Algo", "[k]DECLARE[/k] [c]{var}[/c]").format(var=stmt.variable)
        else:
            ret = translate("Algo", "[k]VARIABLE[/k] [c]{var}[/c] [k]TAKES VALUE[/k] [c]{value}[/c]").format(
                var=code(stmt.variable),
                value=code(stmt.value))

    elif isinstance(stmt, CallStmt):
        ret = translate("Algo", "[k]CALL[/k] [c]{code}[/c]").format(code=code(stmt.to_node()))

    elif isinstance(stmt, ForStmt):
        ret = translate("Algo",
                        "[b]FOR[/b] [c]{var}[/c] [b]FROM[/b] [c]{begin}[/c] [b]TO[/b] [c]{end}[/c] {step}").format(
            var=stmt.variable, begin=code(stmt.begin), end=code(stmt.end),
            step="" if stmt.step is None else translate("Algo", "([b]STEP[/b] [c]{step}[/c])").format(
                step=code(stmt.step)))

    elif isinstance(stmt, FuncStmt):
        ret = translate("Algo", "[b]FUNCTION[/b] [c]{func}({args})[/c]").format(func=stmt.name,
                                                                                args=", ".join(stmt.parameters))

    elif isinstance(stmt, ReturnStmt):
        ret = translate("Algo", "[k]RETURN[/k] [c]{val}[/c]").format(
            val="" if stmt.value is None else code(stmt.value))

    elif isinstance(stmt, StopStmt):
        ret = translate("Algo", "[k]STOP[/k] [c]{val}[/c]").format(
            val="" if stmt.message is None else code(stmt.message))

    elif isinstance(stmt, SleepStmt):
        ret = translate("Algo", "[k]WAIT[/k] [c]{val}[/c] [k]SECONDS[/k]").format(val=code(stmt.duration))

    elif isinstance(stmt, CommentStmt):
        ret = "[t]{com}[/t]".format(com=util.html.sanitize(stmt.content))

    elif isinstance(stmt, GClearStmt):
        ret = translate("Algo", "[k]CLEAR PLOT[/k]")

    elif isinstance(stmt, GLineStmt):
        ret = translate("Algo",
                        "[k]DRAW LINE[/k] [c]{color}[/c] [k]FROM[/k] ([c]{start_x}[/c]; [c]{start_y}[/c]) [k]TO[/k] ([c]{end_x}[/c]; [c]{end_y}[/c])").format(
            color=code(stmt.color),
            start_x=code(stmt.start_x),
            start_y=code(stmt.start_y),
            end_x=code(stmt.end_x),
            end_y=code(stmt.end_y)
        )

    elif isinstance(stmt, GPointStmt):
        ret = translate("Algo", "[k]DRAW POINT[/k] [c]{color}[/c] [k]AT[/k] ([c]{x}[/c]; [c]{y}[/c])").format(
            color=code(stmt.color),
            x=code(stmt.x),
            y=code(stmt.y),
        )

    elif isinstance(stmt, GWindowStmt):
        ret = translate("Algo",
                        "[k]SET WINDOW[/k] [i]Xmin=[/i][c]{x_min}[/c] [i]Xmax=[/i][c]{x_max}[/c] [i]Ymin=[/i][c]{y_min}[/c] [i]Ymax=[/i][c]{y_max}[/c] [i]Xgrad=[/i][c]{x_grad}[/c] [i]Ygrad=[/i][c]{y_grad}[/c]").format(
            x_min=code(stmt.x_min),
            x_max=code(stmt.x_max),
            y_min=code(stmt.y_min),
            y_max=code(stmt.y_max),
            x_grad=code(stmt.x_grad),
            y_grad=code(stmt.y_grad),
        )

    elif isinstance(stmt, GFuncStmt):
        ret = translate("Algo",
                        "[k]PLOT FUNCTION[/k] [c]{color}[/c] [i]f[/i]({var}) = [c]{expr}[/c] [k]FROM[/k] [c]{begin}[/c] [k]TO[/k] [c]{end}[/c] [k]STEP[/k] [c]{step}[/c]").format(
            color=code(stmt.color),
            var=stmt.var,
            expr=code(stmt.expr),
            begin=code(stmt.start),
            end=code(stmt.end),
            step=code(stmt.step)
        )

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

    ret = ret.replace("[g]", "<b>").replace("[/g]", "</b>")
    ret = ret.replace("[n]", "<i>" + red_html).replace("[/n]", "</span></i>")
    ret = ret.replace("[s]", red_html).replace("[/s]", "</span>")

    ret = util.html.unescape_brackets(ret)
    ret = ret.replace("  ", " ")

    return ret.strip()


def store_line(item: QTreeWidgetItem, stmt: BaseStmt):
    item_map[id(stmt)] = item, stmt


def add_block(block: BlockStmt, current, add=False):
    current.append(0)

    for child in block.children:
        add_line(current, child, add=add)

        if isinstance(child, BlockStmt):
            add_block(child, current, add)

        current[-1] += 1

    current.pop()


def load_block(stmt: BlockStmt):
    global item_map
    item_map = {}
    ui.treeWidget.clear()

    global root_item, algo
    algo = stmt
    root_item, lbl = get_item_html(str_stmt(algo))
    ui.treeWidget.addTopLevelItem(root_item)
    store_line(root_item, algo)
    ui.treeWidget.setItemWidget(root_item, 0, lbl)

    current = []

    add_block(stmt, current)

    ui.treeWidget.expandAll()


def load_pseudocode(algo):
    code = eval(algo)
    load_block(code)


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


def algo_double_click():
    if ui.btnAlgo_Edit.isEnabled():
        btn_edit_line()


def algo_sel_changed():
    current = get_current_pos()
    current_stmt = get_current_stmt()

    is_item = current_stmt is not None
    is_root = current == []
    is_changeable = is_item and not is_root
    is_editable = is_changeable and not isinstance(current_stmt,
                                                   (BreakStmt, ContinueStmt, ElseStmt)) and type(
        current_stmt) not in [BaseStmt, BlockStmt]

    ui.btnAlgo_Delete.setEnabled(is_changeable)
    ui.btnAlgo_Edit.setEnabled(is_editable)
    ui.btnAlgo_Dupl.setEnabled(is_changeable and not isinstance(current_stmt, ElseStmt))

    can_up = is_changeable and current != [0]
    ui.btnAlgo_UpBlock.setEnabled(can_up)
    ui.btnAlgo_Up.setEnabled(can_up)

    can_down = is_changeable and current != [len(algo.children) - 1]
    ui.btnAlgo_Down.setEnabled(can_down)
    ui.btnAlgo_DownBlock.setEnabled(can_down)

    ui.btnAlgo_Variable.setEnabled(is_item)
    ui.btnAlgo_Display.setEnabled(is_item)
    ui.btnAlgo_Input.setEnabled(is_item)
    ui.btnAlgo_Call.setEnabled(is_item)
    ui.btnAlgo_Func.setEnabled(is_item)
    ui.btnAlgo_Return.setEnabled(is_changeable)
    ui.btnAlgo_Stop.setEnabled(is_item)
    ui.btnAlgo_Sleep.setEnabled(is_item)

    ui.btnAlgo_If.setEnabled(is_item)
    ui.btnAlgo_Else.setEnabled(is_changeable)
    ui.btnAlgo_For.setEnabled(is_item)
    ui.btnAlgo_While.setEnabled(is_item)
    ui.btnAlgo_Continue.setEnabled(is_changeable)
    ui.btnAlgo_Break.setEnabled(is_changeable)
    ui.btnAlgo_Comment.setEnabled(is_item)
    ui.btnAlgo_GClear.setEnabled(is_item)
    ui.btnAlgo_GWindow.setEnabled(is_item)
    ui.btnAlgo_GPoint.setEnabled(is_item)
    ui.btnAlgo_GLine.setEnabled(is_item)
    ui.btnAlgo_GFunc.setEnabled(is_item)

    if is_changeable:
        parent_stack = [algo]
        for p in current:
            parent_stack.append(parent_stack[-1].children[p])

        existing_else = current[-1] + 1 < len(parent_stack[-2].children) and isinstance(
            parent_stack[-2].children[current[-1] + 1], ElseStmt)

        ui.btnAlgo_Else.setEnabled(isinstance(current_stmt, IfStmt) and not existing_else)

        in_loop = any(x for x in parent_stack if type(x) in [ForStmt, WhileStmt])
        ui.btnAlgo_Continue.setEnabled(in_loop)
        ui.btnAlgo_Break.setEnabled(in_loop)

        in_func = any(x for x in parent_stack if type(x) == FuncStmt)
        ui.btnAlgo_Return.setEnabled(in_func)


def algo_scroll(event: QWheelEvent):
    if event.modifiers() and Qt.ControlModifier:
        if event.angleDelta().y() > 0:
            handler_ZoomIn()
        elif event.angleDelta().y() < 0:
            handler_ZoomOut()
        event.accept()
    else:
        ui.treeWidget.wheelEventOrig(event)


def fix_qt_shitty_margins():
    for wgt in window.centralWidget().findChildren(QPushButton):
        if wgt.text():
            wgt.setText("  " + wgt.text())
            wgt.setMinimumHeight(28)


def init_ui():
    from forms.ui_mainwindow import Ui_MainWindow
    global window, ui
    window = MainWindowWrapper()
    ui = Ui_MainWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    load_languages()

    global algo_base_font
    algo_base_font = ui.treeWidget.font()

    init_recent_actions()

    load_code_editor()
    load_plot_canvas()
    load_algo()

    init_action_handlers()

    right_corner = QMenuBar()
    ui.menubar.removeAction(ui.menuLanguage.menuAction())
    right_corner.addAction(ui.menuLanguage.menuAction())
    ui.menubar.setCornerWidget(right_corner)
    ui.btnSendInput.clicked.connect(send_user_input)
    ui.btnClearOutput.clicked.connect(clear_output)
    ui.btnPrintOutput.clicked.connect(print_output)
    ui.btnSaveOutput.clicked.connect(save_output)

    ui.btnAlgo_Delete.clicked.connect(btn_delete_line)
    ui.btnAlgo_Edit.clicked.connect(btn_edit_line)
    ui.btnAlgo_UpBlock.clicked.connect(btn_move_up_block)
    ui.btnAlgo_Up.clicked.connect(btn_move_up)
    ui.btnAlgo_Down.clicked.connect(btn_move_down)
    ui.btnAlgo_DownBlock.clicked.connect(btn_move_down_block)

    ui.btnAlgo_Dupl.clicked.connect(btn_dupl_line)

    ui.btnAlgo_Variable.clicked.connect(add_def_variable)
    ui.btnAlgo_Display.clicked.connect(add_display)
    ui.btnAlgo_Input.clicked.connect(add_input)
    ui.btnAlgo_Call.clicked.connect(add_call)
    ui.btnAlgo_Func.clicked.connect(add_def_func)
    ui.btnAlgo_Return.clicked.connect(add_return)
    ui.btnAlgo_Stop.clicked.connect(add_stop_stmt)
    ui.btnAlgo_Sleep.clicked.connect(add_sleep_stmt)

    ui.btnAlgo_If.clicked.connect(add_if_block)
    ui.btnAlgo_Else.clicked.connect(add_else_block)
    ui.btnAlgo_For.clicked.connect(add_for_loop)
    ui.btnAlgo_While.clicked.connect(add_while_loop)
    ui.btnAlgo_Continue.clicked.connect(add_continue_stmt)
    ui.btnAlgo_Break.clicked.connect(add_break_stmt)
    ui.btnAlgo_Comment.clicked.connect(add_comment_stmt)

    ui.btnAlgo_GClear.clicked.connect(add_gclear)
    ui.btnAlgo_GWindow.clicked.connect(add_gwindow)
    ui.btnAlgo_GPoint.clicked.connect(add_gpoint)
    ui.btnAlgo_GLine.clicked.connect(add_gline)
    ui.btnAlgo_GFunc.clicked.connect(add_gfunc)

    ui.treeWidget.itemSelectionChanged.connect(algo_sel_changed)
    ui.treeWidget.itemDoubleClicked.connect(algo_double_click)
    ui.treeWidget.wheelEventOrig = ui.treeWidget.wheelEvent
    ui.treeWidget.wheelEvent = algo_scroll

    ui.tabWidget.currentChanged.connect(change_tab)

    def gen(s):
        return lambda: set_theme(s)

    for theme, (name, func) in theming.themes.items():
        action = QAction(window)
        action.setText(name)
        action.setStatusTip(theme)
        action.setCheckable(True)
        action.triggered.connect(gen(theme))
        ui.menuChangeTheme.addAction(action)

    algo_sel_changed()

    global filters
    filters = {
        "all": translate("MainWindow", "Program file (*.py *.tr *.alg)"),
        "py": translate("MainWindow", "Python file (*.py)"),
        "tr": translate("MainWindow", "Turing program (*.tr)"),
        "alg": translate("MainWindow", "Algobox file (*.alg)")
    }

    init_autosave()

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


def autosave():
    settings.setValue("autosave_type", mode_python)
    settings.setValue("autosave_date", datetime.datetime.now())

    if mode_python:
        settings.setValue("autosave", code_editor.toPlainText())
    else:
        settings.setValue("autosave", repr(algo))


def autosave_tick():
    if app_started:
        if is_modified():
            settings.setValue("dirty", True)
            autosave()
        else:
            settings.setValue("dirty", False)
            autosave_clear()


def init_autosave():
    global autosave_timer
    autosave_timer = QTimer()
    autosave_timer.timeout.connect(autosave_tick)
    autosave_timer.start(1000)


def autosave_load():
    global mode_python
    mode_python = settings.value("autosave_type", type=bool)
    content = settings.value("autosave")

    if mode_python:
        code_editor.setPlainText(content, "", "")
    else:
        load_pseudocode(content)

    refresh()


def autosave_clear():
    settings.setValue("dirty", False)
    settings.remove("autosave")
    settings.remove("autosave_date")
    settings.remove("autosave_type")


def clean_exit():
    autosave_clear()
    code_editor.backend.stop()
    sys.exit()


def handler_SendFeedback():
    QDesktopServices.openUrl(QUrl("https://goo.gl/forms/GVCJoBTQv0jYp3MA3"))


def version_check():
    import json
    import urllib.request
    import re
    global new_version
    result = json.load(urllib.request.urlopen("https://api.github.com/repos/TuringApp/Turing/releases/latest"))
    if result and type(result) == dict and "tag_name" in result:
        version = re.findall(r"[\d.]+", result["tag_name"])[0]
        current = re.findall(r"[\d.]+", __version__)[0]
        from distutils.version import StrictVersion
        if StrictVersion(version) > StrictVersion(current):
            new_version = True


if __name__ == "__main__":
    sys.excepthook = except_hook
    setup_thread_excepthook()

    theming.app = app = QApplication(sys.argv)
    app.setApplicationName("Turing")
    app.setApplicationVersion(__version__)

    settings = QSettings("Turing", "Turing")

    util.translate_backend = translate

    DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())

    if os.name == "nt":
        # fix for ugly font on 7+
        font = QFont("Segoe UI", 9)
        app.setFont(font)

    # noinspection PyUnresolvedReferences
    import turing_rc
    splash = QSplashScreen(QPixmap(":/icon/media/icon_128.png"), Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    init_ui()
    change_language(QLocale.system().name())

    set_theme(settings.value("app_theme", "default"))

    window.show()
    splash.finish(window)

    global new_version
    new_version = False

    thr = threading.Thread(target=version_check, args=())
    thr.start()

    while thr.is_alive():
        app.processEvents()

    if new_version:
        msg = msg_box(translate("MainWindow", "A new version of Turing is available.\nWould you like to download it?"),
                      parent=window)
        if msg.exec_() == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl("https://github.com/TuringApp/Turing/releases/latest"))

    window.raise_()
    window.activateWindow()

    dirty = settings.value("dirty", type=bool)

    if dirty:
        msg = msg_box(translate("MainWindow", "A modified file has been automatically saved.\nWould you like to recover it?"),
                      parent=window)
        if msg.exec_() == QMessageBox.Yes:
            autosave_load()
        else:
            autosave_clear()

    app_started = True

    try:
        exitCode = app.exec_()
    except:
        show_error()
        exitCode = 1
    clean_exit()
