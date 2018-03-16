# -*- coding: utf-8 -*-

import re
from html import escape

import maths.lib
import maths.lib.docs
import util.html
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui_help import Ui_HelpWindow
import translator

translate = QCoreApplication.translate

fns = None
catItems = []


def find_func(name):
    for k in fns:
        for f in fns[k]:
            if f[0] == name:
                return (k, f)
    return None


def func_def_html(f):
    hargs = []

    for a in f[1]:
        cur = "<i><b>%s</b></i>" % a[0]
        if len(a) >= 4:
            cur += "=%s" % a[3]
        hargs.append(cur)

    return "<b>%s</b>(%s)" % (f[0], ", ".join(hargs))


def on_sel(current):
    text = current.text(0).strip()

    if current.parent() is not None:
        cat, f = find_func(text[:text.index("(")])

        name, args, desc = f[:3]
        desc = re.sub(r"{{(\w+)\}\}", "<i><b>\g<1></b></i>", desc)
        desc = re.sub(r"//(\w+)//", "<i>\g<1></i>", desc)

        html = util.html.centered("<h1>%s</h1>" % func_def_html(f))

        html += translate("HelpWindow", "<h2>Arguments:</h2>")
        html += "<ul>"

        if not args:
            html += translate("HelpWindow", "<li>None</li>")
        else:
            for arg in args:
                html += "<li>"
                html += "<i><b>%s</b></i> (%s)" % arg[:2]

                if len(arg) > 2:
                    constr = escape(arg[2])

                    if len(arg) > 3:
                        deft = translate("HelpWindow", "default = %s") % arg[3] if arg[3] is not None else None
                    else:
                        deft = None

                    infos = ", ".join(x for x in [constr, deft] if x)

                    if infos:
                        html += " " + infos

                html += "</li>"

        html += "</ul>"

        if len(f) > 3 and f[3]:
            html += translate("HelpWindow", "<h2>Aliases:</h2>")
            html += "<ul>"

            for al in f[3]:
                html += "<li>%s</li>" % al

            html += "</ul>"

        html += "<p>%s</p>" % escape(desc)
    else:
        html = util.html.centered("<h1>%s</h1>" % text)

        html += translate("HelpWindow", "<h2>Functions:</h2>")
        html += "<ul>"

        for fun in fns[text]:
            html += "<li>%s</li>" % func_def_html(fun)

        html += "</ul>"

    ui.textBrowser.setHtml(html)


def load_funcs():
    global fns
    fns = maths.lib.get_funcs()
    for k in sorted(fns.keys()):
        citem = QTreeWidgetItem()
        citem.setText(0, "%s" % k)
        fnt = citem.font(0)
        fnt.setBold(True)
        citem.setFont(0, fnt)
        items = []
        for f in sorted(fns[k], key=lambda x: x[0]):
            item = QTreeWidgetItem()
            item.setText(0, "%s" % maths.lib.docs.get_func_def(f))
            citem.addChild(item)
            items.append(item)

        ui.listFuncs.addTopLevelItem(citem)
        catItems.append((citem, items))


def clr_search():
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
            ci.setHidden(hid == len(items))


def initUi():
    global window, ui
    window = QDialog()
    ui = Ui_HelpWindow()
    translator.add(ui, window)
    ui.setupUi(window)
    ui.textSearch.textChanged.connect(search_changed)
    ui.btnClear.setVisible(False)
    ui.btnClear.clicked.connect(clr_search)
    ui.splitter.setStretchFactor(0, 1)
    ui.splitter.setStretchFactor(1, 3)
    ui.listFuncs.itemClicked.connect(on_sel)
    load_funcs()
    window.show()


def run():
    initUi()
