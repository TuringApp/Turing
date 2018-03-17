# -*- coding: utf-8 -*-

import re
from html import escape

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import maths.lib
import maths.lib.docs
import translator
import util.html
from ui_help import Ui_HelpWindow
from util.math import proper_str

translate = QCoreApplication.translate

functions = None
catItems = []


def find_function(name):
    for k in functions:
        for f in functions[k]:
            if f[0] == name:
                return k, f
    return None


def func_signature_html(f):
    hargs = []

    for a in f[1]:
        cur = "<i><b>%s</b></i>" % a[0]
        if len(a) >= 4:
            cur += "=%s" % proper_str(a[3])
        hargs.append(cur)

    return "<b>%s</b>(%s)" % (f[0], ", ".join(hargs))


def on_item_select(current):
    text = current.text(0).strip()

    if current.parent() is not None:
        category, function = find_function(text[:text.index("(")])

        name, args, desc = function[:3]
        desc = re.sub(r"{{(\w+)\}\}", "<i><b>\g<1></b></i>", escape(desc))
        desc = re.sub(r"//(\w+)//", "<i>\g<1></i>", desc)

        html = util.html.centered("<h1>%s</h1>" % func_signature_html(function))

        html += translate("HelpWindow", "<h2>Arguments:</h2>")
        html += "<ul>"

        if not args:
            html += translate("HelpWindow", "<li>None</li>")
        else:
            for arg in args:
                html += "<li>"
                html += "<i><b>%s</b></i> (%s)" % arg[:2]

                if len(arg) > 2:
                    constraint = escape(arg[2]) if arg[2] else None

                    if len(arg) > 3:
                        default = translate("HelpWindow", "default = %s") % proper_str(arg[3]) \
                            if arg[3] is not None else None
                    else:
                        default = None

                    arg_infos = ", ".join(x for x in [constraint, default] if x)

                    if arg_infos:
                        html += " " + arg_infos

                html += "</li>"

        html += "</ul>"

        if len(function) > 3 and function[3]:
            html += translate("HelpWindow", "<h2>Aliases:</h2>")
            html += "<ul>"

            for alias in function[3]:
                html += "<li>%s</li>" % alias

            html += "</ul>"

        html += "<p>%s</p>" % desc
    else:
        html = util.html.centered("<h1>%s</h1>" % text)

        html += translate("HelpWindow", "<h2>Functions:</h2>")
        html += "<ul>"

        for function in functions[text]:
            html += "<li>%s</li>" % func_signature_html(function)

        html += "</ul>"

    ui.textBrowser.setHtml(html)


def load_funcs():
    global functions
    functions = maths.lib.get_funcs()
    for k in sorted(functions.keys()):
        item_category = QTreeWidgetItem()
        item_category.setText(0, "%s" % k)

        font = item_category.font(0)
        font.setBold(True)
        item_category.setFont(0, font)

        items = []

        for f in sorted(functions[k], key=lambda x: x[0]):
            item = QTreeWidgetItem()
            item.setText(0, "%s" % maths.lib.docs.get_func_def(f))
            item_category.addChild(item)
            items.append(item)

        ui.listFuncs.addTopLevelItem(item_category)
        catItems.append((item_category, items))


def clear_search_field():
    ui.textSearch.setText("")


def search_changed(txt):
    ui.btnClear.setVisible(bool(txt))

    for ci, items in catItems:
        hid = 0

        for i in items:
            if txt.upper() in i.text(0).upper():
                i.setHidden(False)
            else:
                i.setHidden(True)
                hid += 1

            # if all sub-items are hidden, hide the whole category
            ci.setHidden(hid == len(items))


def init_ui():
    global window, ui
    window = QDialog()
    ui = Ui_HelpWindow()

    translator.add(ui, window)
    ui.setupUi(window)

    ui.textSearch.textChanged.connect(search_changed)

    ui.btnClear.setVisible(False)
    ui.btnClear.clicked.connect(clear_search_field)

    # by default, 25-75 ratio
    ui.splitter.setStretchFactor(0, 1)
    ui.splitter.setStretchFactor(1, 3)

    ui.listFuncs.itemClicked.connect(on_item_select)

    load_funcs()
    window.show()


def run():
    init_ui()
