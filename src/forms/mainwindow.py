# -*- coding: utf-8 -*-

import html
import json
import os
import re
import runpy
import sys
import tempfile
import threading
from datetime import datetime

import numpy as np
import pygments.styles
from PyQt5.QtGui import *
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import AutoLocator, LinearLocator

import pyqode.python.backend
import util.code
import util.html
from algo.stmts import *
from lang import translator
from maths.nodes import *
from maths.parser import quick_parse as parse
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from util import first_found_dir
from util import theming, show_error
from util.widgets import *

translate = QCoreApplication.translate


class AppState():
    current_file: Optional[str] = None
    can_save = False
    autosave_timer: QTimer = None
    mode_python = False
    app_started = False
    algo = BlockStmt([])
    new_version = False


async_import_table = {}


def async_import(module):
    def runner():
        globals()[module] = __import__(module)

    async_import_table[module] = threading.Thread(target=runner, args=())
    async_import_table[module].start()


def async_imported(module):
    return not async_import_table[module].is_alive()


class GuiState():
    window: QMainWindow = None
    ui = None
    code_editor: api.CodeEdit = None
    plot_canvas: FigureCanvas = None
    plot_figure: Figure = None
    plot_axes: Axes = None
    panel_search: panels.SearchAndReplacePanel = None
    syntax_highlighter: modes.PygmentsSyntaxHighlighter = None
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
        "GoToLine"
    ]
    algo_only = [
        "Debug",
        "Step",
        "ConvertToPython"
    ]
    filters = {}
    lng_actions = {}
    item_map = {}
    root_item: QTreeWidgetItem = None
    mode_zoom: modes.ZoomMode = None
    mode_ext_select: modes.ExtendedSelectionMode = None
    panel_folding: panels.FoldingPanel = None
    article_load_widgets = None


class ExecState():
    stop_flag = False
    running = False
    run_started: datetime = None
    skip_step = False
    stopped = False
    last_saved = None
    current_stmt: BaseStmt = None
    python_stopped = False
    recent_actions = None
    recent_buttons = None
    article_buttons = None
    article_list = None
    current_output = ""
    after_output = ""
    user_input: str = None
    worker = None


block_html = lambda: '<span style="color:%s;font-weight:bold">' % theming.algo_colors[0]
comment_html = lambda: '<span style="color:%s;font-style:italic">' % theming.algo_colors[1]
keyword_html = lambda: '<span style="color:%s;font-weight:bold">' % theming.algo_colors[2]
red_html = lambda: '<span style="color:%s">' % theming.algo_colors[3]


def sleep(duration):
    begin = datetime.datetime.now()
    while (datetime.datetime.now() - begin).total_seconds() < duration:
        check_stop()
        QCoreApplication.processEvents()


def sleep_seconds(duration):
    sleep(float(duration))
    plot_update()


def is_empty():
    if AppState.mode_python:
        return not GuiState.code_editor.toPlainText()
    else:
        return AppState.algo.children == []


def is_modified():
    if AppState.mode_python:
        return GuiState.code_editor.toPlainText() != ExecState.last_saved
    else:
        return repr(AppState.algo) != ExecState.last_saved


def handler_ClearRecent():
    util.settings.setValue("recent", json.dumps([]))

    recent_update_text()


def recent_add(path):
    recent = json.loads(util.settings.value("recent", "[]"))
    recent.insert(0, path)
    recent = sorted(list(set(recent)))[0:10]

    util.settings.setValue("recent", json.dumps(recent))

    recent_update_text()


def recent_update_text():
    recent = json.loads(util.settings.value("recent", "[]"))

    recent = [f for f in recent if os.path.isfile(f)]

    util.settings.setValue("recent", json.dumps(recent))

    for i, file in enumerate(recent):
        ExecState.recent_actions[i].setText(os.path.basename(file))
        ExecState.recent_buttons[i].setText(os.path.basename(file))
        _, ext = os.path.splitext(file.lower())

        if ext == ".alg":
            icon = QIcon(":/action/media/algobox.ico")
        elif ext == ".tr":
            icon = GuiState.ui.tabWidget.tabIcon(1)
        elif ext == ".py":
            icon = GuiState.ui.tabWidget.tabIcon(2)
        else:
            icon = QIcon()

        ExecState.recent_actions[i].setIcon(icon)
        ExecState.recent_buttons[i].setIcon(icon)

        ExecState.recent_actions[i].setVisible(True)
        ExecState.recent_buttons[i].setVisible(i < 7)

    for i in range(len(recent), 10):
        ExecState.recent_actions[i].setVisible(False)
        ExecState.recent_buttons[i].setVisible(False)

        ExecState.recent_actions[i].setIcon(QIcon())
        ExecState.recent_buttons[i].setIcon(QIcon())

    fix_qt_shitty_margins()


def recent_clicked(index):
    recent = json.loads(util.settings.value("recent", "[]"))

    if index < len(recent) and recent[index]:
        load_file(recent[index])


def recent_init_actions():
    ExecState.recent_actions = []
    ExecState.recent_buttons = []

    def generator(num):
        return lambda: recent_clicked(num)

    for i in range(10):
        act = QAction(GuiState.window)
        act.setVisible(False)
        act.triggered.connect(generator(i))
        ExecState.recent_actions.append(act)
        GuiState.ui.menuRecent.insertAction(GuiState.ui.actionClearRecent, act)

        btn = QFlatButton(GuiState.window)
        btn.setVisible(False)
        btn.clicked.connect(generator(i))
        ExecState.recent_buttons.append(btn)
        GuiState.ui.verticalLayout_10.addWidget(btn)

    GuiState.ui.menuRecent.insertSeparator(GuiState.ui.actionClearRecent)
    GuiState.ui.verticalLayout_10.addItem(QSpacerItem(1, 2, QSizePolicy.Minimum, QSizePolicy.Expanding))

    recent_update_text()


def article_clicked(i):
    QDesktopServices.openUrl(QUrl(ExecState.article_list[i][1]))


def article_fetch(language):
    import urllib.request
    from xml.etree import ElementTree

    response = urllib.request.urlopen("https://turingapp.ml/%s/feed/" % language)
    xml = ElementTree.fromstring(response.read())
    result = []

    for elem in xml[0].iter("item"):
        result.append((elem.find("title").text, elem.find("link").text))

    return result


def article_init_actions(update=True):
    ExecState.article_buttons = []
    ExecState.article_list = []

    def generator(i):
        return lambda: article_clicked(i)

    for i in range(7):
        btn = QFlatButton(GuiState.window)
        btn.setVisible(False)
        btn.clicked.connect(generator(i))
        ExecState.article_buttons.append(btn)
        GuiState.ui.verticalLayout_11.addWidget(btn)

    GuiState.ui.verticalLayout_11.addItem(QSpacerItem(1, 2, QSizePolicy.Minimum, QSizePolicy.Expanding))

    if update:
        return article_update_text_begin()


def article_remove_button():
    if GuiState.article_load_widgets is not None:
        GuiState.ui.verticalLayout_11.removeWidget(GuiState.article_load_widgets[0])
        GuiState.article_load_widgets[0].deleteLater()
        GuiState.ui.verticalLayout_11.removeItem(GuiState.article_load_widgets[1])
        GuiState.article_load_widgets = None
    for btn in ExecState.article_buttons:
        btn.setVisible(False)


def article_init_button():
    article_remove_button()
    btn = QFlatButton(GuiState.window)
    spacer = QSpacerItem(1, 2, QSizePolicy.Minimum, QSizePolicy.Expanding)
    GuiState.article_load_widgets = (btn, spacer)

    def handler():
        set_load_recent_articles(True)
        article_update_text_begin(True)

    btn.setIcon(QIcon(":/action/media/download.png"))
    btn.setText(translate("MainWindow", "Load recent articles"))
    btn.clicked.connect(handler)
    GuiState.ui.verticalLayout_11.addWidget(btn)
    GuiState.ui.verticalLayout_11.addItem(spacer)


def article_loader():
    ExecState.article_list = article_fetch(translator.current_lang) or article_fetch("")


def article_update_text_begin(both=False):
    article_remove_button()
    thr = threading.Thread(target=article_loader, args=())
    thr.start()
    if both:
        article_update_text_end(thr)
    else:
        return thr


def article_update_text_end(thr=None):
    if thr is not None:
        while thr.is_alive():
            QCoreApplication.processEvents()

    for i, (name, _) in enumerate(ExecState.article_list):
        ExecState.article_buttons[i].setText(name)
        ExecState.article_buttons[i].setVisible(True)

    for i in range(len(ExecState.article_list), 7):
        ExecState.article_buttons[i].setVisible(False)


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
    return getattr(GuiState.ui, "action" + name)


def refresh():
    plot_update()
    refresh_buttons_status()

    if not AppState.mode_python:
        refresh_algo()
        algo_sel_changed()

    refresh_window_title()


def refresh_window_title():
    if GuiState.ui.tabWidget.currentIndex() == 0:
        title = "Turing"
    else:
        if AppState.current_file:
            filename = os.path.basename(AppState.current_file)
            if is_modified():
                title = translate("MainWindow", "Turing - {file} (unsaved)").format(file=filename)
            else:
                title = translate("MainWindow", "Turing - {file}").format(file=filename)
        else:
            title = translate("MainWindow", "Turing - New File")

    GuiState.window.setWindowTitle(title)


def refresh_buttons_status():
    if AppState.mode_python:
        for ours, theirs in GuiState.editor_action_table:
            get_action(ours).setEnabled(getattr(GuiState.code_editor, "action_" + theirs).isEnabled())

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

    for c in GuiState.python_only:
        get_action(c).setVisible(AppState.mode_python)

    for c in GuiState.algo_only:
        get_action(c).setVisible(not AppState.mode_python)

    # if AppState.current_file != -1:
    #    get_action("Undo").setEnabled(undo_objs[AppState.current_file].can_undo())
    #    get_action("Redo").setEnabled(undo_objs[AppState.current_file].can_redo())


def handler_Undo():
    if AppState.mode_python:
        GuiState.code_editor.undo()


def handler_Redo():
    if AppState.mode_python:
        GuiState.code_editor.redo()


def handler_SelectAll():
    GuiState.code_editor.selectAll()


def handler_Cut():
    if AppState.mode_python:
        GuiState.code_editor.cut()


def handler_Copy():
    if AppState.mode_python:
        GuiState.code_editor.copy()


def handler_Paste():
    if AppState.mode_python:
        GuiState.code_editor.paste()


def handler_DuplicateLine():
    if AppState.mode_python:
        GuiState.code_editor.duplicate_line()
    else:
        btn_dupl_line()


def handler_Indent():
    GuiState.code_editor.indent()


def handler_Unindent():
    GuiState.code_editor.un_indent()


def handler_GoToLine():
    GuiState.code_editor.goto_line()


def handler_Find():
    GuiState.panel_search.on_search()


def handler_FindPrevious():
    GuiState.panel_search.select_previous()


def handler_FindNext():
    GuiState.panel_search.select_next()


def handler_Replace():
    GuiState.panel_search.on_search_and_replace()


def handler_Calculator():
    from forms import calculator
    calculator.CalculatorWindow()


def handler_ChangTheme():
    from forms import changtheme

    backup = util.settings.value("app_theme")

    dlg = changtheme.ChangeThemeWindow(GuiState.window, theming.themes[backup][1])
    dlg.theme_callback = lambda: set_theme("custom")

    if dlg.run():
        util.settings.setValue("custom_theme", theming.themes["custom"][1])

        for act in GuiState.ui.menuChangeTheme.actions():
            if act.statusTip() == "custom":
                act.setVisible(True)
                break
    else:
        set_theme(backup)


def handler_HelpContents():
    from forms import help
    help.HelpWindow(GuiState.window)


def change_tab():
    if GuiState.ui.tabWidget.currentIndex() == 1:
        AppState.mode_python = False
    elif GuiState.ui.tabWidget.currentIndex() == 2:
        AppState.mode_python = True

    refresh()


def python_print(*args, end="\n"):
    ExecState.current_output += html.escape(" ".join(str(arg) for arg in args))
    ExecState.current_output += end
    update_output()


def update_output():
    GuiState.ui.txtOutput.setHtml(
        '<pre style="margin: 0">%s</pre>' % (ExecState.current_output + ExecState.after_output))
    GuiState.ui.txtOutput.moveCursor(QTextCursor.End)
    GuiState.ui.txtOutput.ensureCursorVisible()
    if ExecState.current_output.endswith("\n\n"):
        ExecState.current_output = ExecState.current_output[:-1]
    plot_update()


def check_stop():
    if ExecState.stopped or (not AppState.mode_python and ExecState.worker.finished):
        raise KeyboardInterrupt()


def python_input(prompt="", globals=None, locals=None, unsafe=False):
    python_print(prompt, end="")
    plot_update()

    ExecState.after_output = "<hr>"
    ExecState.after_output += util.html.centered(
        "<h3>%s</h3>" % util.html.color_span("<i>%s</i>" % translate("MainWindow", "Input: ") + html.escape(prompt),
                                             "red"))
    update_output()

    GuiState.ui.btnSendInput.setEnabled(True)
    GuiState.ui.txtInput.setEnabled(True)
    GuiState.ui.txtInput.setFocus(Qt.OtherFocusReason)

    for n in range(3):
        if not GuiState.ui.txtInput.text():
            GuiState.ui.txtInput.setStyleSheet("QLineEdit { background-color: #ffbaba; }")
            sleep(0.050)
            GuiState.ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
            sleep(0.050)
            GuiState.ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff5252; }")
            sleep(0.050)
            GuiState.ui.txtInput.setStyleSheet("QLineEdit { background-color: #ff7b7b; }")
            sleep(0.050)
            GuiState.ui.txtInput.setStyleSheet("QLineEdit { background-color: #ffbaba; }")
            sleep(0.050)

        GuiState.ui.txtInput.setStyleSheet("")
        sleep(0.200)

    ExecState.user_input = None

    while ExecState.user_input is None:
        check_stop()
        QCoreApplication.processEvents()

    GuiState.ui.btnSendInput.setEnabled(False)
    GuiState.ui.txtInput.setEnabled(False)
    GuiState.ui.txtInput.setText("")

    ExecState.after_output = ""
    python_print(ExecState.user_input)
    update_output()

    if unsafe:
        try:
            evaled = eval(ExecState.user_input, globals, locals)
            return evaled
        except:
            pass

    try:
        to_int = int(ExecState.user_input)
        return to_int
    except:
        pass

    try:
        to_float = float(ExecState.user_input)
        return to_float
    except:
        pass

    if unsafe:
        try:
            to_complex = complex(ExecState.user_input)
            return to_complex
        except:
            pass

    return ExecState.user_input


def python_print_error(msg, end="\n"):
    ExecState.current_output += util.html.color_span(msg, "red") + end

    if not AppState.mode_python:
        set_current_line(ExecState.worker.last, True)

    update_output()


def plot_update():
    if GuiState.plot_axes is not None and GuiState.plot_canvas is not None:
        GuiState.plot_axes.grid(linestyle='-')
        GuiState.plot_canvas.draw()


def plot_clear():
    GuiState.plot_axes.clear()
    GuiState.plot_axes.axhline(y=0, color='k')
    GuiState.plot_axes.axvline(x=0, color='k')


def plot_reset():
    plot_clear()
    plot_window(-10, 10, -10, 10)
    plot_update()


def plot_window(xmin, xmax, ymin, ymax, xgrad=0, ygrad=0):
    GuiState.plot_axes.set_xlim(xmin, xmax)
    GuiState.plot_axes.set_ylim(ymin, ymax)

    GuiState.plot_axes.get_xaxis().set_major_locator(
        AutoLocator() if xgrad == 0 else LinearLocator(abs(int((xmax - xmin) / xgrad)) + 1))
    GuiState.plot_axes.get_yaxis().set_major_locator(
        AutoLocator() if ygrad == 0 else LinearLocator(abs(int((ymax - ymin) / ygrad)) + 1))


def plot_point(x, y, color="red"):
    GuiState.plot_axes.scatter([x], [y], c=color)


def plot_line(startx, starty, endx, endy, color="red"):
    GuiState.plot_axes.plot([startx, endx], [starty, endy], c=color, linestyle="-", marker="o")


def plot_function(func, start, end, step, color="red"):
    domain = [x.item() for x in np.arange(start, end, step)]
    results = [func(x) for x in domain]
    GuiState.plot_axes.plot(domain, results, c=color, linestyle="-")


def stmt_GClear(stmt: GClearStmt):
    plot_clear()


def stmt_GWindow(stmt: GWindowStmt):
    plot_window(ExecState.worker.evaluator.eval_node(stmt.x_min),
                ExecState.worker.evaluator.eval_node(stmt.x_max),
                ExecState.worker.evaluator.eval_node(stmt.y_min),
                ExecState.worker.evaluator.eval_node(stmt.y_max),
                ExecState.worker.evaluator.eval_node(stmt.x_grad),
                ExecState.worker.evaluator.eval_node(stmt.y_grad))


def stmt_GPoint(stmt: GPointStmt):
    plot_point(ExecState.worker.evaluator.eval_node(stmt.x), ExecState.worker.evaluator.eval_node(stmt.y),
               ExecState.worker.evaluator.eval_node(stmt.color))


def stmt_GLine(stmt: GLineStmt):
    plot_line(ExecState.worker.evaluator.eval_node(stmt.start_x),
              ExecState.worker.evaluator.eval_node(stmt.start_y),
              ExecState.worker.evaluator.eval_node(stmt.end_x),
              ExecState.worker.evaluator.eval_node(stmt.end_y),
              ExecState.worker.evaluator.eval_node(stmt.color))


def stmt_GFunc(stmt: GFuncStmt):
    plot_function(ExecState.worker.evaluator.eval_node(stmt.get_function()),
                  ExecState.worker.evaluator.eval_node(stmt.start),
                  ExecState.worker.evaluator.eval_node(stmt.end),
                  ExecState.worker.evaluator.eval_node(stmt.step),
                  ExecState.worker.evaluator.eval_node(stmt.color))


def stmt_Sleep(stmt: SleepStmt):
    sleep_seconds(ExecState.worker.evaluator.eval_node(stmt.duration))


def init_worker():
    from algo.worker import Worker
    ExecState.worker = Worker(AppState.algo.children)
    ExecState.worker.callback_print = python_print
    ExecState.worker.callback_input = python_input
    ExecState.worker.log.set_callback(python_print_error)
    ExecState.worker.log.use_prefix = False
    ExecState.worker.init()
    ExecState.worker.callback_stop = callback_stop
    ExecState.worker.map[GClearStmt] = stmt_GClear
    ExecState.worker.map[GWindowStmt] = stmt_GWindow
    ExecState.worker.map[GPointStmt] = stmt_GPoint
    ExecState.worker.map[GLineStmt] = stmt_GLine
    ExecState.worker.map[GFuncStmt] = stmt_GFunc
    ExecState.worker.map[SleepStmt] = stmt_Sleep
    set_current_line(None)
    plot_reset()


def end_output():
    ExecState.current_output += util.html.centered(
        util.html.color_span(translate("MainWindow", "end of output") if ExecState.run_started is None
                             else translate("MainWindow", "end of output [{time}]").format(
            time=datetime.datetime.now() - ExecState.run_started), "red"))
    ExecState.current_output += "<hr />\n"
    ExecState.run_started = None
    update_output()


def set_current_line(current: Optional[BaseStmt], error=False):
    for item, stmt in GuiState.item_map.values():
        if stmt == current:
            item.setBackground(0, QBrush(QColor("#ef5350") if error else QColor("#fdd835")))
        else:
            item.setBackground(0, GuiState.root_item.background(0))


def callback_stop(stmt, virtual=False):
    breakpoint_message(ExecState.worker.evaluator.eval_node(stmt.message))
    if not virtual:
        ExecState.worker.finished = True


def breakpoint_message(message=""):
    ExecState.after_output = "<hr>"
    ExecState.after_output += util.html.centered(
        "<h3>%s</h3>" % util.html.color_span("<i>%s</i>" % (
            translate("MainWindow", "Breakpoint: ") + html.escape(str(message)) if message else translate("MainWindow",
                                                                                                          "Breakpoint")),
                                             "red"))
    update_output()


def python_breakpoint(message=""):
    breakpoint_message(message)

    ExecState.python_stopped = True

    GuiState.ui.actionRun.setDisabled(False)
    GuiState.ui.actionStop.setDisabled(False)

    while ExecState.python_stopped and not ExecState.stopped:
        QCoreApplication.processEvents()

    if ExecState.stopped:
        raise KeyboardInterrupt()

    ExecState.after_output = ""
    update_output()

    GuiState.ui.actionRun.setDisabled(True)
    GuiState.ui.actionStop.setDisabled(True)


def handler_Stop():
    python_print_error(translate("MainWindow", "program interrupted"))
    ExecState.after_output = ""
    ExecState.stopped = True
    if AppState.mode_python:
        ExecState.running = False
        ExecState.python_stopped = False
    else:
        ExecState.running = True
        ExecState.worker.finished = True
        ExecState.worker.error = False
        ExecState.stop_flag = True
        handler_Step()
        ExecState.stop_flag = False
    update_output()


def handler_Step():
    GuiState.ui.actionNew.setDisabled(True)
    GuiState.ui.actionOpen.setDisabled(True)
    GuiState.ui.actionRun.setDisabled(True)
    GuiState.ui.actionDebug.setDisabled(True)
    GuiState.ui.actionStep.setDisabled(True)
    GuiState.ui.actionStop.setEnabled(True)

    try:
        if AppState.mode_python:
            pass
        else:
            if not ExecState.stopped:
                if ExecState.running:
                    if ExecState.skip_step:
                        ExecState.skip_step = False
                        ExecState.after_output = ""
                        update_output()
                    else:
                        if isinstance(ExecState.current_stmt, StopStmt):
                            callback_stop(ExecState.current_stmt, True)
                            ExecState.skip_step = True
                        else:
                            ExecState.worker.exec_stmt(ExecState.current_stmt)
                else:
                    init_worker()
                    ExecState.running = True

                if not ExecState.skip_step and not ExecState.worker.error:
                    ExecState.current_stmt = ExecState.worker.next_stmt()

                    set_current_line(ExecState.current_stmt)
            else:
                ExecState.stopped = False

        QCoreApplication.processEvents()
        plot_update()
    except:
        show_error()
    finally:
        plot_update()
        if ExecState.worker.finished:
            GuiState.ui.actionRun.setDisabled(False)
            if not ExecState.stop_flag:
                end_output()
            if not ExecState.worker.error:
                set_current_line(None)
            ExecState.running = False
        GuiState.ui.actionDebug.setDisabled(False)
        GuiState.ui.actionStep.setDisabled(False)
        GuiState.ui.actionNew.setDisabled(not ExecState.worker.finished)
        GuiState.ui.actionOpen.setDisabled(not ExecState.worker.finished)
        GuiState.ui.actionStop.setEnabled(not ExecState.worker.finished)


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
    if ExecState.python_stopped:
        ExecState.python_stopped = False
        return

    if not flag and not AppState.mode_python:
        algo_run_python()
        return

    GuiState.ui.actionNew.setDisabled(True)
    GuiState.ui.actionOpen.setDisabled(True)
    GuiState.ui.actionRun.setDisabled(True)
    GuiState.ui.actionDebug.setDisabled(True)
    GuiState.ui.actionStep.setDisabled(True)
    GuiState.ui.actionStop.setEnabled(True)
    user_stop = False
    set_current_line(None)
    try:
        if AppState.mode_python:
            file = tempfile.NamedTemporaryFile(mode="w+b", suffix=".py", delete=False)
            try:
                code = util.code.python_wrapper(GuiState.code_editor.toPlainText()).encode("utf8")
                file.write(code)
                file.close()
                ExecState.running = True
                ExecState.stopped = False
                ExecState.python_stopped = False
                plot_reset()
                ExecState.run_started = datetime.datetime.now()
                runpy.run_path(file.name, init_globals={
                    "print": python_print,
                    "input": python_input,
                    "breakpoint": python_breakpoint,
                    "list": compat_list,
                    "sleep": sleep_seconds,

                    "g_clear": plot_clear,
                    "g_window": plot_window,
                    "g_point": plot_point,
                    "g_line": plot_line,
                    "g_func": plot_function,

                    "plot": GuiState.plot_axes
                })
                plot_update()
            except SyntaxError as err:
                msg = translate("MainWindow", "Syntax error ({type}) at line {line}, offset {off}: ").format(
                    type=type(err).__name__, line=err.lineno - util.code.line_offset, off=err.offset)
                python_print_error(msg + html.escape(err.text), end="")
                python_print_error(" " * (len(msg) + err.offset - 1) + "↑")
            except KeyboardInterrupt:
                pass
            except:
                python_print_error(html.escape(str(sys.exc_info()[1])))
            finally:
                os.unlink(file.name)
                plot_update()
        else:
            if not ExecState.running:
                init_worker()
                plot_reset()
                ExecState.worker.break_on_error = True
                ExecState.running = True
                ExecState.stopped = False
                ExecState.run_started = datetime.datetime.now()
                ExecState.skip_step = False
            else:
                if ExecState.skip_step:
                    ExecState.skip_step = False
                    ExecState.after_output = ""
                    update_output()
                else:
                    ExecState.worker.exec_stmt(ExecState.current_stmt)
                    if not ExecState.worker.error:
                        set_current_line(None)

            while not ExecState.worker.finished:
                ExecState.worker.step()
                QCoreApplication.processEvents()
    except KeyboardInterrupt:
        user_stop = True
    except:
        show_error()
    finally:
        plot_update()
        if not AppState.mode_python and ExecState.worker.stopped:
            GuiState.ui.actionStep.setDisabled(False)
            GuiState.ui.actionDebug.setDisabled(False)
            set_current_line(ExecState.worker.last)
            ExecState.skip_step = True
            ExecState.worker.finished = False
            ExecState.worker.stopped = False
        else:
            if not user_stop:
                end_output()
            GuiState.ui.actionNew.setDisabled(False)
            GuiState.ui.actionOpen.setDisabled(False)
            GuiState.ui.actionRun.setDisabled(False)
            GuiState.ui.actionStep.setDisabled(False)
            GuiState.ui.actionDebug.setDisabled(False)
            GuiState.ui.actionStop.setEnabled(False)
            ExecState.running = False


def load_python_code():
    import autopep8
    py_code = autopep8.fix_code("\n".join(AppState.algo.python()))
    GuiState.code_editor.setPlainText(py_code.replace("\t", "    "), "", "")


def handler_ConvertToPython():
    load_python_code()
    AppState.mode_python = True
    AppState.current_file = None
    refresh()


def algo_run_python():
    load_python_code()
    AppState.mode_python = True
    handler_Run()
    AppState.mode_python = False
    # GuiState.code_editor.setPlainText("", "", "")


def handler_AboutTuring():
    import forms.about
    forms.about.AboutWindow(GuiState.window, util.__version__, util.__channel__).run()


def handler_Examples():
    """
    callback function for actionExamples.
    Let the user choose one example file, providing some metadata
    about examples to make an easier choice.
    """
    msg = msg_box_info(translate("MainWindow",
                                 "You are about to choose an example file\nfrom the `examples` directory. To guess what examples are,\nyou can guess from the file names."))
    msg.exec_()
    data_dirs = ["/usr/share/turing/",
                 os.path.dirname(os.path.realpath(__file__)),
                 os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                 os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))] + \
                QStandardPaths.standardLocations(QStandardPaths.DataLocation) + \
                QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)
    data_dirs = [os.path.join(x, "examples") for x in data_dirs]
    handler_Open(whichDir=first_found_dir(data_dirs))
    return


def set_show_toolbar(show):
    if show:
        GuiState.ui.toolBar.show()
    else:
        GuiState.ui.toolBar.hide()

    util.settings.setValue("show_toolbar", show)
    GuiState.ui.actionShowToolbar.setChecked(show)


def handler_ShowToolbar():
    set_show_toolbar(not GuiState.ui.toolBar.isVisible())


def set_show_toolbar_text(show):
    if show:
        GuiState.ui.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    else:
        GuiState.ui.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)

    util.settings.setValue("show_toolbar_text", show)
    GuiState.ui.actionShowToolbarText.setChecked(show)


def handler_ShowToolbarText():
    set_show_toolbar_text(GuiState.ui.toolBar.toolButtonStyle() == Qt.ToolButtonIconOnly)


def save(filename):
    if AppState.mode_python:
        ExecState.last_saved = str(GuiState.code_editor.toPlainText())
    else:
        ExecState.last_saved = repr(AppState.algo)

    with open(filename, "w+", encoding="utf8") as savefile:
        savefile.write(ExecState.last_saved)

    recent_add(filename)

    refresh()


def save_output():
    file = QFileDialog.getSaveFileName(GuiState.window, translate("MainWindow", "Save output"),
                                       "",
                                       translate("MainWindow", "Text files (*.txt)"))[0]
    if not file:
        return

    with open(file, "w+", encoding="utf8") as savefile:
        savefile.write(GuiState.ui.txtOutput.toPlainText())


def handler_SaveAs():
    file = QFileDialog.getSaveFileName(GuiState.window, translate("MainWindow", "Save"),
                                       "",
                                       GuiState.filters[["tr", "py"][AppState.mode_python]])[0]
    if not file:
        return

    AppState.current_file = file
    handler_Save()


def handler_Save():
    if not AppState.current_file:
        handler_SaveAs()
        return
    try:
        save(AppState.current_file)
    except PermissionError:
        msg = msg_box_info(
            translate("MainWindow", "You are not allowed to write to {},\nplease choose another file path.").format(
                AppState.current_file))
        msg.exec_()
        handler_SaveAs()
    return


def handler_Open(whichDir=""):
    """
    callback function to open a file
    @param whichDir the directory to browse initially
    """
    sel_file, _ = QFileDialog.getOpenFileName(
        GuiState.window, translate("MainWindow", "Open"),
        whichDir,
        ";;".join(GuiState.filters.values()))

    if not sel_file:
        return

    load_file(sel_file)


def load_file(file):
    AppState.current_file = file
    _, ext = os.path.splitext(AppState.current_file.lower())

    with open(AppState.current_file, "r", encoding="utf8") as openfile:
        newcode = openfile.read()

    if ext == ".alg":
        from algo.frontends.algobox import parse_algobox
        AppState.mode_python = False
        load_block(parse_algobox(newcode))
        ExecState.last_saved = repr(AppState.algo)

    elif ext == ".tr":
        AppState.mode_python = False
        load_pseudocode(newcode)
        ExecState.last_saved = repr(AppState.algo)

    elif ext == ".py":
        AppState.mode_python = True
        GuiState.code_editor.setPlainText(newcode, "", "")
        ExecState.last_saved = newcode

    recent_add(AppState.current_file)

    set_correct_tab()

    refresh()


def set_correct_tab():
    GuiState.ui.tabWidget.setCurrentIndex(2 if AppState.mode_python else 1)


def handler_New():
    if is_modified():
        msg = msg_box(
            translate("MainWindow", "Do you really want to create a new file?\nAll unsaved changes will be lost."),
            parent=GuiState.window)
        if msg.exec_() != QMessageBox.Yes:
            return

    AppState.current_file = None
    AppState.algo = BlockStmt([])
    GuiState.code_editor.setPlainText("", "", "")

    set_correct_tab()

    refresh()


def handler_ZoomIn():
    if AppState.mode_python:
        GuiState.code_editor.zoom_in()
    else:
        set_algo_size(GuiState.ui.treeWidget.font().pointSize() + 1)


def handler_ZoomOut():
    if AppState.mode_python:
        GuiState.code_editor.zoom_out()
    else:
        set_algo_size(GuiState.ui.treeWidget.font().pointSize() - 1)


def handler_ResetZoom():
    if AppState.mode_python:
        GuiState.code_editor.reset_zoom()
    else:
        set_algo_size(GuiState.algo_base_font.pointSize())


def set_algo_size(size):
    if size < 1:
        size = 1
    set_font_size(GuiState.ui.treeWidget, size)
    for idstmt, (item, stmt) in GuiState.item_map.items():
        set_font_size(item, size, 0)
        if hasattr(item, "lbl"):
            set_font_size(item.lbl, size)


def init_action_handlers():
    for item in dir(GuiState.ui):
        if item.startswith("action"):
            name = "handler_" + item[6:]

            if name in globals():
                getattr(GuiState.ui, item).triggered.connect(globals()[name])


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
        act = QAction(GuiState.window)
        act.setCheckable(True)
        act.setIcon(QIcon(cur))
        act.setText(locale.nativeLanguageName())
        act.triggered.connect(gen(locale_name))
        GuiState.ui.menuLanguage.addAction(act)
        GuiState.lng_actions[locale_name] = act


def fix_tabwidget_width():
    GuiState.ui.tabWidget_2.setMinimumWidth(
        sum(GuiState.ui.tabWidget_2.tabBar().tabRect(x).width() for x in range(GuiState.ui.tabWidget_2.count())))
    GuiState.ui.widget.setMinimumWidth(0)
    GuiState.ui.widget.setMaximumWidth(16777215)
    GuiState.ui.widget.adjustSize()
    width = max(GuiState.window.width() / 3, GuiState.ui.widget.width())
    GuiState.ui.widget.setMinimumWidth(width)
    GuiState.ui.widget.setMaximumWidth(width)


def refresh_locs():
    for act in GuiState.ui.menuChangeTheme.actions():
        if act.statusTip():
            act.setText(theming.themes[act.statusTip()][0]())


def change_language(language: str):
    available = GuiState.lng_actions.keys()

    if language not in available:
        if util.get_short_lang(language) in available:
            language = util.get_short_lang(language)
        else:
            language = "en"

    translator.load(language)

    GuiState.ui.menubar.resizeEvent(QResizeEvent(GuiState.ui.menubar.size(), GuiState.ui.menubar.size()))
    load_editor_actions()

    for l, a in GuiState.lng_actions.items():
        a.setChecked(l == language)

    fix_qt_shitty_margins()
    fix_tabwidget_width()

    if sys.platform == "darwin":
        GuiState.ui.menuLanguage.setTitle(QLocale(language).nativeLanguageName())

    if util.settings.value("load_articles", False, type=bool):
        thr = article_update_text_begin()
    else:
        article_init_button()

    refresh_locs()
    refresh()

    if util.settings.value("load_articles", False, type=bool):
        article_update_text_end(thr)


def send_user_input():
    ExecState.user_input = GuiState.ui.txtInput.text()


def clear_output():
    ExecState.current_output = ""
    if not AppState.mode_python:
        set_current_line(None)
    update_output()
    plot_reset()


def print_output():
    print(dir(GuiState.code_editor))

    p = QGuiApplication.palette()
    print(p.color(QPalette.Window).name())
    print(p.color(QPalette.WindowText).name())
    print(p.color(QPalette.Disabled, QPalette.WindowText).name())
    print(p.color(QPalette.Base).name())
    print(p.color(QPalette.AlternateBase).name())
    print(p.color(QPalette.ToolTipBase).name())
    print(p.color(QPalette.ToolTipText).name())
    print(p.color(QPalette.Text).name())
    print(p.color(QPalette.Disabled, QPalette.Text).name())
    print(p.color(QPalette.Dark).name())
    print(p.color(QPalette.Shadow).name())
    print(p.color(QPalette.Button).name())
    print(p.color(QPalette.ButtonText).name())
    print(p.color(QPalette.Disabled, QPalette.ButtonText).name())
    print(p.color(QPalette.BrightText).name())
    print(p.color(QPalette.Link).name())
    print(p.color(QPalette.Highlight).name())
    print(p.color(QPalette.Disabled, QPalette.Highlight).name())
    print(p.color(QPalette.HighlightedText).name())
    print(p.color(QPalette.Disabled, QPalette.HighlightedText).name())

    theming.themes["devtest"] = (theming.themes["devtest"][0], GuiState.code_editor.toPlainText().split("\n"))
    set_theme("devtest")

    pass


def load_editor_actions():
    for ours, theirs in GuiState.editor_action_table:
        copy_action(getattr(GuiState.ui, "action" + ours), getattr(GuiState.code_editor, "action_" + theirs))

    # edge cases
    copy_action(GuiState.ui.actionFind, GuiState.panel_search.menu.menuAction())
    GuiState.code_editor._sub_menus["Advanced"].setTitle(translate("MainWindow", "Advanced"))
    GuiState.mode_zoom.mnu_zoom.setTitle(translate("MainWindow", "Zoom"))

    GuiState.panel_folding.context_menu.setTitle(translate("MainWindow", "Folding"))
    GuiState.panel_folding.context_menu.actions()[0].setText(translate("MainWindow", "Collapse"))
    GuiState.panel_folding.context_menu.actions()[1].setText(translate("MainWindow", "Expand"))
    GuiState.panel_folding.context_menu.actions()[3].setText(translate("MainWindow", "Collapse all"))
    GuiState.panel_folding.context_menu.actions()[4].setText(translate("MainWindow", "Expand all"))

    GuiState.mode_ext_select.action_select_word.setText(translate("MainWindow", "Select word"))
    GuiState.mode_ext_select.action_select_extended_word.setText(translate("MainWindow", "Select extended word"))
    GuiState.mode_ext_select.action_select_matched.setText(translate("MainWindow", "Matched select"))
    GuiState.mode_ext_select.action_select_line.setText(translate("MainWindow", "Select line"))
    GuiState.mode_ext_select.action_select_line.associatedWidgets()[0].setTitle(translate("MainWindow", "Select"))

    GuiState.panel_search.labelSearch.setPixmap(GuiState.ui.actionFind.icon().pixmap(16, 16))
    GuiState.panel_search.labelSearch.setMaximumSize(QSize(16, 16))
    GuiState.panel_search.labelReplace.setPixmap(GuiState.ui.actionReplace.icon().pixmap(16, 16))
    GuiState.panel_search.labelReplace.setMaximumSize(QSize(16, 16))
    GuiState.panel_search.toolButtonPrevious.setIcon(QIcon(":/action/media/up.png"))
    GuiState.panel_search.toolButtonNext.setIcon(QIcon(":/action/media/down.png"))
    GuiState.panel_search.toolButtonClose.setIcon(QIcon(":/action/media/cross.png"))

    GuiState.panel_search.checkBoxRegex.setText(translate("MainWindow", "Regex"))
    GuiState.panel_search.checkBoxCase.setText(translate("MainWindow", "Match case"))
    GuiState.panel_search.checkBoxWholeWords.setText(translate("MainWindow", "Whole words"))
    GuiState.panel_search.checkBoxInSelection.setText(translate("MainWindow", "In Selection"))
    GuiState.panel_search.labelMatches.setText(translate("MainWindow", "0 matches"))
    GuiState.panel_search.toolButtonReplace.setText(translate("MainWindow", "Replace"))
    GuiState.panel_search.toolButtonReplaceAll.setText(translate("MainWindow", "Replace All"))
    GuiState.panel_search.lineEditSearch.prompt_text = translate("MainWindow", "Find")
    GuiState.panel_search.lineEditSearch.button.setIcon(QIcon(":/action/media/backspace.png"))
    GuiState.panel_search.lineEditSearch.button.setMinimumSize(QSize(21, 21))
    GuiState.panel_search.lineEditReplace.prompt_text = translate("MainWindow", "Replace")
    GuiState.panel_search.lineEditReplace.button.setIcon(QIcon(":/action/media/backspace.png"))


def copy_actions_to_editor(panel):
    for name, obj in panel.__dict__.items():
        if name.startswith("action_"):
            setattr(GuiState.code_editor, name, obj)
        elif name.startswith("action"):  # workaround for shitty naming by the devs
            setattr(GuiState.code_editor, "action_" + name[6:], obj)


def set_theme(theme):
    if theme not in theming.themes or not theming.themes[theme][1]:
        theme = "default"

    util.settings.setValue("app_theme", theme)
    theming.load_theme(theme)

    for act in GuiState.ui.menuChangeTheme.actions():
        act.setChecked(act.statusTip() == theme)

    refresh_algo()


def set_style(style):
    util.settings.setValue("editor_style", style)
    GuiState.syntax_highlighter.pygments_style = style

    for act in GuiState.ui.menuChangeStyle.actions():
        act.setChecked(act.text() == style)


def load_code_editor():
    GuiState.code_editor = api.CodeEdit()
    if hasattr(sys, "frozen"):
        print("using external backend")
        if sys.platform == "win32":
            backend = "editor_backend.exe"
        elif sys.platform.startswith("linux"):
            backend = "editor_backend"
        elif sys.platform == "darwin":
            backend = "editor_backend"
        backend = os.path.join(sys._MEIPASS, backend)
    else:
        print("using script file")

        while not async_imported("editor_backend"):
            QCoreApplication.processEvents()

        backend = globals()["editor_backend"].__file__
    GuiState.code_editor.backend.start(backend)
    GuiState.code_editor.modes.append(modes.CodeCompletionMode())
    GuiState.code_editor.modes.append(modes.CaretLineHighlighterMode())
    GuiState.code_editor.modes.append(modes.AutoCompleteMode())
    GuiState.code_editor.modes.append(modes.IndenterMode())
    GuiState.code_editor.modes.append(modes.AutoIndentMode())
    GuiState.code_editor.modes.append(modes.OccurrencesHighlighterMode())
    GuiState.code_editor.modes.append(modes.SmartBackSpaceMode())
    GuiState.code_editor.modes.append(modes.SymbolMatcherMode())
    GuiState.mode_zoom = modes.ZoomMode()
    GuiState.code_editor.modes.append(GuiState.mode_zoom)
    GuiState.code_editor.action_zoom_in = GuiState.mode_zoom.mnu_zoom.actions()[0]
    GuiState.code_editor.action_zoom_out = GuiState.mode_zoom.mnu_zoom.actions()[1]
    GuiState.code_editor.action_reset_zoom = GuiState.mode_zoom.mnu_zoom.actions()[2]

    GuiState.mode_ext_select = GuiState.code_editor.modes.append(modes.ExtendedSelectionMode())

    GuiState.syntax_highlighter = GuiState.code_editor.modes.append(
        modes.PygmentsSyntaxHighlighter(GuiState.code_editor.document()))
    GuiState.syntax_highlighter.fold_detector = api.IndentFoldDetector()

    GuiState.panel_folding = GuiState.code_editor.panels.append(panels.FoldingPanel())
    GuiState.code_editor.panels.append(panels.LineNumberPanel())
    GuiState.code_editor.modes.append(modes.CheckerMode(pyqode.python.backend.run_pep8))
    GuiState.code_editor.panels.append(panels.GlobalCheckerPanel(), panels.GlobalCheckerPanel.Position.LEFT)
    GuiState.panel_search = GuiState.code_editor.panels.append(panels.SearchAndReplacePanel(),
                                                               api.Panel.Position.BOTTOM)

    GuiState.panel_search._update_label_matches_orig = GuiState.panel_search._update_label_matches

    def wrapper():
        GuiState.panel_search._update_label_matches_orig()
        if GuiState.panel_search.labelMatches.text():
            GuiState.panel_search.labelMatches.setText(
                translate("MainWindow", "{num} matches").format(num=GuiState.panel_search.cpt_occurences))

    GuiState.panel_search._update_label_matches = wrapper

    copy_actions_to_editor(GuiState.panel_search)

    GuiState.code_editor.textChanged.connect(refresh)

    load_editor_actions()

    def gen(s):
        return lambda: set_style(s)

    for style in pygments.styles.get_all_styles():
        action = QAction(GuiState.window)
        action.setText(style)
        action.setCheckable(True)
        action.triggered.connect(gen(style))
        GuiState.ui.menuChangeStyle.addAction(action)

    GuiState.syntax_highlighter.pygments_style = util.settings.value("editor_style", "default")
    set_style(GuiState.syntax_highlighter.pygments_style)

    GuiState.ui.verticalLayout_8.addWidget(GuiState.code_editor)


def load_plot_canvas():
    GuiState.plot_figure = Figure()
    GuiState.plot_axes = GuiState.plot_figure.add_subplot(111)
    GuiState.plot_canvas = FigureCanvas(GuiState.plot_figure)
    plot_reset()
    GuiState.ui.verticalLayout_4.addWidget(GuiState.plot_canvas)


def get_item_label(item):
    def gen_func(item):
        return lambda: GuiState.ui.treeWidget.setCurrentItem(item)

    txt = QClickableLabel()
    txt.setStyleSheet(GuiState.ui.treeWidget.styleSheet())
    txt.clicked.connect(gen_func(item))
    txt.dclicked.connect(algo_double_click)
    item.lbl = txt
    GuiState.ui.treeWidget.setItemWidget(item, 0, txt)
    GuiState.ui.treeWidget.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    return txt


def get_item_html(html, data=""):
    item = QTreeWidgetItem()
    item.setStatusTip(0, data)
    item.setFont(0, GuiState.ui.treeWidget.font())
    lbl = get_item_label(item)
    lbl.setFont(item.font(0))
    lbl.setText('&nbsp;<span>%s</span>' % html)

    GuiState.ui.treeWidget.setItemWidget(item, 0, lbl)

    return item, lbl


def refresh_algo_text():
    for item, stmt in GuiState.item_map.values():
        lbl = get_item_label(item)
        lbl.setText('&nbsp;<span>%s</span>' % str_stmt(stmt))


def add_display():
    from forms import alg_display
    dlg = alg_display.AlgoDisplayStmt(GuiState.window)
    if dlg.run():
        append_line(DisplayStmt(dlg.expr, dlg.newline))


def add_def_variable():
    from forms import alg_define
    dlg = alg_define.AlgoDefineStmt(GuiState.window)
    if dlg.run():
        append_line(AssignStmt(dlg.varname, dlg.expr))


def add_input():
    from forms import alg_input
    dlg = alg_input.AlgoInputStmt(GuiState.window)
    if dlg.run():
        append_line(InputStmt(dlg.varname, dlg.expr, dlg.text))


def add_call():
    from forms import alg_call
    dlg = alg_call.AlgoCallStmt(GuiState.window)
    if dlg.run():
        append_line(CallStmt(dlg.func, dlg.args))


def add_def_func():
    from forms import alg_func
    dlg = alg_func.AlgoFuncStmt(GuiState.window)
    if dlg.run():
        append_line(FuncStmt(dlg.func, dlg.args, []))


def add_return():
    from forms import alg_return
    dlg = alg_return.AlgoReturnStmt(GuiState.window)
    if dlg.run():
        append_line(ReturnStmt(dlg.expr))


def add_if_block():
    from forms import alg_if
    dlg = alg_if.AlgoIfStmt(GuiState.window)
    if dlg.run():
        append_line(IfStmt(dlg.expr, []))


def add_else_block():
    append_line(ElseStmt([]))


def add_for_loop():
    from forms import alg_for
    dlg = alg_for.AlgoForStmt(GuiState.window)
    if dlg.run():
        append_line(ForStmt(dlg.varname, dlg.f_from, dlg.f_to, [], dlg.f_step))


def add_while_loop():
    from forms import alg_while
    dlg = alg_while.AlgoWhileStmt(GuiState.window)
    if dlg.run():
        append_line(WhileStmt(dlg.expr, []))


def add_gclear():
    append_line(GClearStmt())


def add_gline():
    from forms import alg_gline
    dlg = alg_gline.AlgoGLineStmt(GuiState.window)
    if dlg.run():
        append_line(GLineStmt(dlg.f_start_x, dlg.f_start_y, dlg.f_end_x, dlg.f_end_y, dlg.f_color))


def add_gpoint():
    from forms import alg_gpoint
    dlg = alg_gpoint.AlgoGPointStmt(GuiState.window)
    if dlg.run():
        append_line(GPointStmt(dlg.f_x, dlg.f_y, dlg.f_color))


def add_gwindow():
    from forms import alg_gwindow
    dlg = alg_gwindow.AlgoGWindowStmt(GuiState.window)
    if dlg.run():
        append_line(GWindowStmt(dlg.f_x_min, dlg.f_x_max, dlg.f_y_min, dlg.f_y_max, dlg.f_x_grad, dlg.f_y_grad))


def add_gfunc():
    from forms import alg_gfunc
    dlg = alg_gfunc.AlgoGFuncStmt(GuiState.window)
    if dlg.run():
        append_line(GFuncStmt(dlg.f_variable, dlg.f_function, dlg.f_start, dlg.f_end, dlg.f_step, dlg.f_color))


def add_break_stmt():
    append_line(BreakStmt())


def add_continue_stmt():
    append_line(ContinueStmt())


def add_stop_stmt():
    from forms import alg_stop
    dlg = alg_stop.AlgoStopStmt(GuiState.window)
    if dlg.run():
        append_line(StopStmt(dlg.expr))


def add_sleep_stmt():
    from forms import alg_sleep
    dlg = alg_sleep.AlgoSleepStmt(GuiState.window)
    if dlg.run():
        append_line(SleepStmt(dlg.expr))


def add_comment_stmt():
    from forms import alg_comment
    dlg = alg_comment.AlgoCommentStmt(GuiState.window)
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
        dlg = alg_display.AlgoDisplayStmt(GuiState.window, (stmt.content.code(), stmt.newline))
        if dlg.run():
            stmt.content = dlg.expr
            stmt.newline = dlg.newline

    elif isinstance(stmt, CallStmt):
        from forms import alg_call
        dlg = alg_call.AlgoCallStmt(GuiState.window, (stmt.function.code(), [x.code() for x in stmt.arguments]))
        if dlg.run():
            stmt.function = dlg.func
            stmt.arguments = dlg.args

    elif isinstance(stmt, AssignStmt):
        from forms import alg_define
        dlg = alg_define.AlgoDefineStmt(GuiState.window, (stmt.variable.code(), stmt.value.code()))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.value = dlg.expr

    elif isinstance(stmt, ReturnStmt):
        from forms import alg_return
        dlg = alg_return.AlgoReturnStmt(GuiState.window, stmt.value.code() if stmt.value is not None else None)
        if dlg.run():
            stmt.value = dlg.expr

    elif isinstance(stmt, StopStmt):
        from forms import alg_stop
        dlg = alg_stop.AlgoStopStmt(GuiState.window, stmt.message.code() if stmt.message is not None else None)
        if dlg.run():
            stmt.message = dlg.expr

    elif isinstance(stmt, SleepStmt):
        from forms import alg_sleep
        dlg = alg_sleep.AlgoSleepStmt(GuiState.window, stmt.duration.code())
        if dlg.run():
            stmt.duration = dlg.expr

    elif isinstance(stmt, InputStmt):
        from forms import alg_input
        dlg = alg_input.AlgoInputStmt(GuiState.window,
                                      (stmt.variable.code(), stmt.prompt.code() if stmt.prompt is not None else None,
                                       stmt.text))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.prompt = dlg.expr
            stmt.text = dlg.text

    elif isinstance(stmt, IfStmt):
        from forms import alg_if
        dlg = alg_if.AlgoIfStmt(GuiState.window, stmt.condition.code())
        if dlg.run():
            stmt.condition = dlg.expr

    elif isinstance(stmt, WhileStmt):
        from forms import alg_while
        dlg = alg_while.AlgoWhileStmt(GuiState.window, stmt.condition.code())
        if dlg.run():
            stmt.condition = dlg.expr

    elif isinstance(stmt, ForStmt):
        from forms import alg_for
        dlg = alg_for.AlgoForStmt(GuiState.window, (
            stmt.variable, stmt.begin.code(), stmt.end.code(), stmt.step.code() if stmt.step is not None else None))
        if dlg.run():
            stmt.variable = dlg.varname
            stmt.begin = dlg.f_from
            stmt.end = dlg.f_to
            stmt.step = dlg.f_step

    elif isinstance(stmt, FuncStmt):
        from forms import alg_func
        dlg = alg_func.AlgoFuncStmt(GuiState.window, (stmt.name, stmt.parameters))
        if dlg.run():
            stmt.name = dlg.func
            stmt.parameters = dlg.args

    elif isinstance(stmt, CommentStmt):
        from forms import alg_comment
        dlg = alg_comment.AlgoCommentStmt(GuiState.window, stmt.content)
        if dlg.run():
            stmt.content = dlg.comment

    elif isinstance(stmt, GLineStmt):
        from forms import alg_gline
        dlg = alg_gline.AlgoGLineStmt(GuiState.window, (
            stmt.start_x.code(), stmt.start_y.code(), stmt.end_x.code(), stmt.end_y.code(), stmt.color.code()))
        if dlg.run():
            stmt.start_x = dlg.f_start_x
            stmt.start_y = dlg.f_start_y
            stmt.end_x = dlg.f_end_x
            stmt.end_y = dlg.f_end_y
            stmt.color = dlg.f_color

    elif isinstance(stmt, GPointStmt):
        from forms import alg_gpoint
        dlg = alg_gpoint.AlgoGPointStmt(GuiState.window, (stmt.x.code(), stmt.y.code(), stmt.color.code()))
        if dlg.run():
            stmt.x = dlg.f_x
            stmt.y = dlg.f_y
            stmt.color = dlg.f_color

    elif isinstance(stmt, GWindowStmt):
        from forms import alg_gwindow
        dlg = alg_gwindow.AlgoGWindowStmt(GuiState.window, (
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
        dlg = alg_gfunc.AlgoGFuncStmt(GuiState.window, (
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
        existing = AppState.algo

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
    current_item = GuiState.ui.treeWidget.currentItem()

    if current_item is not None:
        for item, stmt in GuiState.item_map.values():
            if item == current_item:
                return stmt

    return AppState.algo


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
        find_block(AppState.algo)

    return current


def get_parent(pos):
    parent = GuiState.root_item
    parent_stmt = AppState.algo

    for p in pos[:-1]:
        parent = parent.child(p)
        parent_stmt = parent_stmt.children[p]

    return parent, parent_stmt


def set_current_stmt(current):
    if current is None:
        return

    for item, stmt in GuiState.item_map.values():
        if stmt == current:
            GuiState.ui.treeWidget.setCurrentItem(item)
            break


def refresh_algo():
    current = None
    line = GuiState.ui.treeWidget.currentItem()
    for item, stmt in GuiState.item_map.values():
        if item == line:
            current = stmt
            break

    load_block(AppState.algo)

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

    GuiState.ui.treeWidget.setItemWidget(item, 0, lbl)


def handler_UseArrowNotation():
    util.settings.setValue("use_arrow_notation", GuiState.ui.actionUseArrowNotation.isChecked())
    refresh_algo()


def set_load_recent_articles(val):
    GuiState.ui.actionLoadRecentArticles.setChecked(val)
    util.settings.setValue("load_articles", val)


def handler_LoadRecentArticles():
    set_load_recent_articles(GuiState.ui.actionLoadRecentArticles.isChecked())


def handler_CheckForUpdates():
    util.settings.setValue("check_for_updates", GuiState.ui.actionCheckForUpdates.isChecked())

    if GuiState.ui.actionCheckForUpdates.isChecked():
        run_updater()


def str_stmt(stmt):
    code = lambda stmt: stmt.code(True)

    if isinstance(stmt, DisplayStmt):
        ret = translate("Algo", "[k]DISPLAY[/k] [c]{val}[/c] {newline}").format(val=code(stmt.content),
                                                                                newline="↵" if stmt.newline else "")

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
        ret = translate("Algo", "[k]INPUT[/k] [c]{prompt}[/c] [k]TO[/k] [c]{var}[/c] {text}").format(
            prompt="" if stmt.prompt is None else stmt.prompt.code(True), var=code(stmt.variable),
            text="⌘" if stmt.text else "")

    elif isinstance(stmt, AssignStmt):
        if stmt.value is None:
            ret = translate("Algo", "[k]DECLARE[/k] [c]{var}[/c]").format(var=stmt.variable)
        else:
            ret = (translate("Algo", "[c]{var}[/c] [k]&#129128;[/k] [c]{value}[/c]")
                   if GuiState.ui.actionUseArrowNotation.isChecked()
                   else translate("Algo", "[k]VARIABLE[/k] [c]{var}[/c] [k]TAKES VALUE[/k] [c]{value}[/c]")).format(
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

    ret = ret.replace("[b]", block_html()).replace("[/b]", "</span>")
    ret = ret.replace("[k]", keyword_html()).replace("[/k]", "</span>")
    ret = ret.replace("[c]", "<code>").replace("[/c]", "</code>")
    ret = ret.replace("[i]", "<i>").replace("[/i]", "</i>")
    ret = ret.replace("[t]", comment_html()).replace("[/t]", "</span>")

    ret = ret.replace("[g]", "<b>").replace("[/g]", "</b>")
    ret = ret.replace("[n]", "<i>" + red_html()).replace("[/n]", "</span></i>")
    ret = ret.replace("[s]", red_html()).replace("[/s]", "</span>")

    ret = util.html.unescape_brackets(ret)
    ret = ret.replace("  ", " ")

    return ret.strip()


def store_line(item: QTreeWidgetItem, stmt: BaseStmt):
    GuiState.item_map[id(stmt)] = item, stmt


def add_block(block: BlockStmt, current, add=False):
    current.append(0)

    for child in block.children:
        add_line(current, child, add=add)

        if isinstance(child, BlockStmt):
            add_block(child, current, add)

        current[-1] += 1

    current.pop()


def load_block(stmt: BlockStmt):
    GuiState.item_map = {}
    GuiState.ui.treeWidget.clear()

    AppState.algo = stmt
    GuiState.root_item, lbl = get_item_html(str_stmt(AppState.algo))
    GuiState.ui.treeWidget.addTopLevelItem(GuiState.root_item)
    store_line(GuiState.root_item, AppState.algo)
    GuiState.ui.treeWidget.setItemWidget(GuiState.root_item, 0, lbl)

    current = []

    add_block(stmt, current)

    GuiState.ui.treeWidget.expandAll()


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
    if GuiState.ui.btnAlgo_Edit.isEnabled():
        btn_edit_line()


def algo_sel_changed():
    current = get_current_pos()
    current_stmt = get_current_stmt()

    is_item = current_stmt is not None
    is_root = current == []
    is_changeable = is_item and not is_root
    is_editable = is_changeable \
                  and not isinstance(current_stmt, (BreakStmt, ContinueStmt, ElseStmt)) \
                  and type(current_stmt) not in [BaseStmt, BlockStmt]

    GuiState.ui.btnAlgo_Delete.setEnabled(is_changeable)
    GuiState.ui.btnAlgo_Edit.setEnabled(is_editable)
    GuiState.ui.btnAlgo_Dupl.setEnabled(is_changeable and not isinstance(current_stmt, ElseStmt))

    can_up = is_changeable and current != [0]
    GuiState.ui.btnAlgo_UpBlock.setEnabled(can_up)
    GuiState.ui.btnAlgo_Up.setEnabled(can_up)

    can_down = is_changeable and current != [len(AppState.algo.children) - 1]
    GuiState.ui.btnAlgo_Down.setEnabled(can_down)
    GuiState.ui.btnAlgo_DownBlock.setEnabled(can_down)

    GuiState.ui.btnAlgo_Variable.setEnabled(is_item)
    GuiState.ui.btnAlgo_Display.setEnabled(is_item)
    GuiState.ui.btnAlgo_Input.setEnabled(is_item)
    GuiState.ui.btnAlgo_Call.setEnabled(is_item)
    GuiState.ui.btnAlgo_Func.setEnabled(is_item)
    GuiState.ui.btnAlgo_Return.setEnabled(is_changeable)
    GuiState.ui.btnAlgo_Stop.setEnabled(is_item)
    GuiState.ui.btnAlgo_Sleep.setEnabled(is_item)

    GuiState.ui.btnAlgo_If.setEnabled(is_item)
    GuiState.ui.btnAlgo_Else.setEnabled(is_changeable)
    GuiState.ui.btnAlgo_For.setEnabled(is_item)
    GuiState.ui.btnAlgo_While.setEnabled(is_item)
    GuiState.ui.btnAlgo_Continue.setEnabled(is_changeable)
    GuiState.ui.btnAlgo_Break.setEnabled(is_changeable)
    GuiState.ui.btnAlgo_Comment.setEnabled(is_item)
    GuiState.ui.btnAlgo_GClear.setEnabled(is_item)
    GuiState.ui.btnAlgo_GWindow.setEnabled(is_item)
    GuiState.ui.btnAlgo_GPoint.setEnabled(is_item)
    GuiState.ui.btnAlgo_GLine.setEnabled(is_item)
    GuiState.ui.btnAlgo_GFunc.setEnabled(is_item)

    if is_changeable:
        parent_stack = [AppState.algo]
        for p in current:
            parent_stack.append(parent_stack[-1].children[p])

        existing_else = current[-1] + 1 < len(parent_stack[-2].children) and isinstance(
            parent_stack[-2].children[current[-1] + 1], ElseStmt)

        GuiState.ui.btnAlgo_Else.setEnabled(isinstance(current_stmt, IfStmt) and not existing_else)

        in_loop = any(x for x in parent_stack if type(x) in [ForStmt, WhileStmt])
        GuiState.ui.btnAlgo_Continue.setEnabled(in_loop)
        GuiState.ui.btnAlgo_Break.setEnabled(in_loop)

        in_func = any(x for x in parent_stack if type(x) == FuncStmt)
        GuiState.ui.btnAlgo_Return.setEnabled(in_func)


def algo_scroll(event: QWheelEvent):
    if event.modifiers() and Qt.ControlModifier:
        if event.angleDelta().y() > 0:
            handler_ZoomIn()
        elif event.angleDelta().y() < 0:
            handler_ZoomOut()

        event.accept()
    else:
        GuiState.ui.treeWidget.wheelEventOrig(event)


def fix_qt_shitty_margins():
    for wgt in GuiState.window.centralWidget().findChildren(QPushButton):
        if not wgt.icon().isNull() and wgt.text() and not wgt.text().startswith("  "):
            wgt.setText("  " + wgt.text())

        wgt.setMinimumHeight(28)


def init_theme_actions():
    def gen(s):
        return lambda: set_theme(s)

    for theme in theming.themes:
        action = QAction(GuiState.window)
        action.setStatusTip(theme)
        action.setCheckable(True)
        action.triggered.connect(gen(theme))
        GuiState.ui.menuChangeTheme.addAction(action)

        if theme == "custom":
            action.setVisible(bool(theming.themes["custom"][1]))


def load_home_actions():
    def gen(btn, a):
        def func():
            btn.setEnabled(a.isEnabled())
            btn.setText(a.text())

        return func

    for a in [GuiState.ui.actionNew, GuiState.ui.actionOpen]:
        btn = QFlatButton(GuiState.window)
        btn.setIcon(a.icon())
        btn.clicked.connect(a.triggered)
        a.changed.connect(gen(btn, a))
        GuiState.ui.verticalLayout_3.addWidget(btn)


def init_ui():
    from forms.ui_mainwindow import Ui_MainWindow
    GuiState.window = MainWindowWrapper()
    GuiState.ui = Ui_MainWindow()

    translator.add(GuiState.ui, GuiState.window)
    GuiState.ui.setupUi(GuiState.window)

    load_languages()

    GuiState.algo_base_font = GuiState.ui.treeWidget.font()

    recent_init_actions()

    article_thr = article_init_actions(util.settings.value("load_articles", False, type=bool))

    if article_thr is None:
        article_init_button()

    load_home_actions()

    load_code_editor()
    load_plot_canvas()
    load_algo()

    init_action_handlers()

    if sys.platform != "darwin":
        right_corner = QMenuBar()
        GuiState.ui.menubar.removeAction(GuiState.ui.menuLanguage.menuAction())
        right_corner.addAction(GuiState.ui.menuLanguage.menuAction())
        GuiState.ui.menubar.setCornerWidget(right_corner)

    init_event_handlers()

    init_theme_actions()

    algo_sel_changed()

    GuiState.filters = {
        "all": translate("MainWindow", "Program file (*.py *.tr *.alg)"),
        "py": translate("MainWindow", "Python file (*.py)"),
        "tr": translate("MainWindow", "Turing program (*.tr)"),
        "alg": translate("MainWindow", "Algobox file (*.alg)")
    }

    autosave_init()

    set_show_toolbar(util.settings.value("show_toolbar", True, type=bool))
    set_show_toolbar_text(util.settings.value("show_toolbar_text", True, type=bool))

    GuiState.ui.actionUseArrowNotation.setChecked(util.settings.value("use_arrow_notation", False, type=bool))

    is_deb = False

    if os.path.exists("/etc/issue"):
        try:
            with open("/etc/issue", encoding="utf-8") as fp:
                issue = fp.read()

            if re.match("Debian", issue, re.M) or re.match("Ubuntu", issue, re.M):
                is_deb = True
        except:
            pass

    GuiState.ui.actionLoadRecentArticles.setChecked(util.settings.value("load_articles", False, type=bool))
    GuiState.ui.actionCheckForUpdates.setChecked(util.settings.value("check_for_updates", not is_deb, type=bool))

    center_widget(GuiState.window, None)
    fix_qt_shitty_margins()

    if util.settings.value("load_articles", False, type=bool):
        article_update_text_end(article_thr)

    GuiState.window.show()


def init_event_handlers():
    GuiState.ui.btnSendInput.clicked.connect(send_user_input)
    GuiState.ui.btnClearOutput.clicked.connect(clear_output)
    GuiState.ui.btnPrintOutput.clicked.connect(print_output)
    GuiState.ui.btnSaveOutput.clicked.connect(save_output)

    GuiState.ui.btnAlgo_Delete.clicked.connect(btn_delete_line)
    GuiState.ui.btnAlgo_Edit.clicked.connect(btn_edit_line)
    GuiState.ui.btnAlgo_UpBlock.clicked.connect(btn_move_up_block)
    GuiState.ui.btnAlgo_Up.clicked.connect(btn_move_up)
    GuiState.ui.btnAlgo_Down.clicked.connect(btn_move_down)
    GuiState.ui.btnAlgo_DownBlock.clicked.connect(btn_move_down_block)

    GuiState.ui.btnAlgo_Dupl.clicked.connect(btn_dupl_line)

    GuiState.ui.btnAlgo_Variable.clicked.connect(add_def_variable)
    GuiState.ui.btnAlgo_Display.clicked.connect(add_display)
    GuiState.ui.btnAlgo_Input.clicked.connect(add_input)
    GuiState.ui.btnAlgo_Call.clicked.connect(add_call)
    GuiState.ui.btnAlgo_Func.clicked.connect(add_def_func)
    GuiState.ui.btnAlgo_Return.clicked.connect(add_return)
    GuiState.ui.btnAlgo_Stop.clicked.connect(add_stop_stmt)
    GuiState.ui.btnAlgo_Sleep.clicked.connect(add_sleep_stmt)

    GuiState.ui.btnAlgo_If.clicked.connect(add_if_block)
    GuiState.ui.btnAlgo_Else.clicked.connect(add_else_block)
    GuiState.ui.btnAlgo_For.clicked.connect(add_for_loop)
    GuiState.ui.btnAlgo_While.clicked.connect(add_while_loop)
    GuiState.ui.btnAlgo_Continue.clicked.connect(add_continue_stmt)
    GuiState.ui.btnAlgo_Break.clicked.connect(add_break_stmt)
    GuiState.ui.btnAlgo_Comment.clicked.connect(add_comment_stmt)

    GuiState.ui.btnAlgo_GClear.clicked.connect(add_gclear)
    GuiState.ui.btnAlgo_GWindow.clicked.connect(add_gwindow)
    GuiState.ui.btnAlgo_GPoint.clicked.connect(add_gpoint)
    GuiState.ui.btnAlgo_GLine.clicked.connect(add_gline)
    GuiState.ui.btnAlgo_GFunc.clicked.connect(add_gfunc)

    GuiState.ui.treeWidget.itemSelectionChanged.connect(algo_sel_changed)
    GuiState.ui.treeWidget.itemDoubleClicked.connect(algo_double_click)

    GuiState.ui.treeWidget.wheelEventOrig = GuiState.ui.treeWidget.wheelEvent
    GuiState.ui.treeWidget.wheelEvent = algo_scroll

    GuiState.ui.tabWidget.currentChanged.connect(change_tab)


def autosave_write():
    util.settings.setValue("autosave_type", AppState.mode_python)
    util.settings.setValue("autosave_date", datetime.datetime.now())

    if AppState.mode_python:
        content = GuiState.code_editor.toPlainText()
    else:
        content = repr(AppState.algo)

    util.settings.setValue("autosave_content", content)


def autosave_tick():
    if AppState.app_started:
        if is_modified():
            util.settings.setValue("autosave_dirty", True)
            autosave_write()
        else:
            util.settings.setValue("autosave_dirty", False)
            autosave_clear()


def autosave_init():
    AppState.autosave_timer = QTimer()
    AppState.autosave_timer.timeout.connect(autosave_tick)
    AppState.autosave_timer.start(1000)


def autosave_load():
    AppState.mode_python = util.settings.value("autosave_type", False, type=bool)
    content = util.settings.value("autosave_content", "")

    if AppState.mode_python:
        GuiState.code_editor.setPlainText(content, "", "")
    else:
        load_pseudocode(content)

    refresh()


def autosave_clear():
    util.settings.setValue("autosave_dirty", False)
    util.settings.remove("autosave_content")
    util.settings.remove("autosave_date")
    util.settings.remove("autosave_type")


def clean_exit():
    autosave_clear()
    GuiState.code_editor.backend.stop()
    sys.exit()


def handler_SendFeedback():
    QDesktopServices.openUrl(QUrl("https://goo.gl/forms/GVCJoBTQv0jYp3MA3"))


def version_check():
    import json
    import urllib.request
    import re

    result = json.load(urllib.request.urlopen("https://api.github.com/repos/TuringApp/Turing/releases/latest"))

    if result and type(result) == dict and "tag_name" in result:
        version = re.findall(r"[\d.]+", result["tag_name"])[0]
        current = re.findall(r"[\d.]+", util.__version__)[0]
        from distutils.version import StrictVersion

        if StrictVersion(version) > StrictVersion(current):
            AppState.new_version = True


def run_updater():
    AppState.new_version = False

    thr = threading.Thread(target=version_check, args=())
    thr.start()

    while thr.is_alive():
        QCoreApplication.processEvents()

    if AppState.new_version:
        msg = msg_box(translate("MainWindow", "A new version of Turing is available.\nWould you like to download it?"),
                      parent=GuiState.window)
        if msg.exec_() == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl("https://github.com/TuringApp/Turing/releases/latest"))


def autosave_check():
    dirty = util.settings.value("autosave_dirty", False, type=bool)

    if dirty:
        msg = msg_box(
            translate("MainWindow", "A modified file has been automatically saved.\nWould you like to recover it?"),
            parent=GuiState.window)
        if msg.exec_() == QMessageBox.Yes:
            autosave_load()
        else:
            autosave_clear()


def init_pre():
    if not hasattr(sys, "frozen"):
        async_import("editor_backend")


init_pre()


def init_main(splash):
    init_ui()

    set_theme(util.settings.value("app_theme", "default"))

    change_language(QLocale.system().name())

    GuiState.window.show()
    splash.finish(GuiState.window)

    if GuiState.ui.actionCheckForUpdates.isChecked():
        run_updater()

    GuiState.window.raise_()
    GuiState.window.activateWindow()

    autosave_check()

    AppState.app_started = True
