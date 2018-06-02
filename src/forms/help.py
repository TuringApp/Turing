# -*- coding: utf-8 -*-

import re
from html import escape

import maths.lib
import maths.lib.docs
import util.html
from forms.ui_help import Ui_HelpWindow
from lang import translator
from util.math import proper_str
from util.widgets import *

translate = QCoreApplication.translate


class HelpWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.ui = Ui_HelpWindow()

        translator.add(self.ui, self)
        self.ui.setupUi(self)

        self.ui.textSearch.textChanged.connect(self.search_changed)

        self.ui.btnClear.setVisible(False)
        self.ui.btnClear.clicked.connect(self.clear_search_field)

        # by default, 25-75 ratio
        self.ui.splitter.setStretchFactor(0, 2)
        self.ui.splitter.setStretchFactor(1, 5)

        self.ui.listFuncs.itemSelectionChanged.connect(self.on_item_select)

        self.load_funcs()
        self.show()

    def on_item_select(self):
        current = self.ui.listFuncs.currentItem()

        if current.parent() is not None:
            category, function = maths.lib.find_function(current.statusTip(0))

            name, args, desc = function[:3]
            desc = re.sub(r"{{(\w+)\}\}", "<i><b>\g<1></b></i>", escape(desc))
            desc = re.sub(r"//(\w+)//", "<i>\g<1></i>", desc)

            html = util.html.centered("<h1>%s</h1>" % maths.lib.docs.get_func_def_html(function))

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
                            default = translate("HelpWindow", "default = {deft}").format(
                                deft=proper_str(arg[3]) if arg[3] is not None else None)
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
            text = current.text(0).strip()
            html = util.html.centered("<h1>%s</h1>" % text)

            html += translate("HelpWindow", "<h2>Functions:</h2>")
            html += "<ul>"

            for function in self.functions[text]:
                html += "<li>%s</li>" % maths.lib.docs.get_func_def_html(function)

            html += "</ul>"

        self.ui.textBrowser.setHtml(html)

    def load_funcs(self):
        self.functions = maths.lib.get_funcs()
        self.catItems = []
        for k in sorted(self.functions.keys()):
            item_category = QTreeWidgetItem()
            item_category.setText(0, "%s" % k)

            font = item_category.font(0)
            font.setBold(True)
            item_category.setFont(0, font)

            items = []

            def gen_func(item):
                return lambda: self.ui.listFuncs.setCurrentItem(item)

            for f in sorted(self.functions[k], key=lambda x: x[0]):
                item = QTreeWidgetItem(item_category)
                item.setStatusTip(0, f[0])
                txt = QClickableLabel()
                txt.setText("&nbsp;" + maths.lib.docs.get_func_def_html(f, False))
                txt.clicked.connect(gen_func(item))
                self.ui.listFuncs.setItemWidget(item, 0, txt)
                items.append(item)

                self.ui.listFuncs.addTopLevelItem(item_category)
            self.catItems.append((item_category, items))

    def clear_search_field(self):
        self.ui.textSearch.setText("")

    def search_changed(self, txt: str):
        self.ui.btnClear.setVisible(bool(txt))

        for ci, items in self.catItems:
            hid = 0

            for i in items:
                if txt.upper() in i.statusTip(0).upper():
                    i.setHidden(False)
                else:
                    i.setHidden(True)
                    hid += 1

                # if all sub-items are hidden, hide the whole category
                ci.setHidden(hid == len(items))
