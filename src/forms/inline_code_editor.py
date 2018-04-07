# -*- coding: utf-8 -*-
import html
import re
from typing import Tuple, Dict, List

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import maths.lib.docs
from forms.w_inline_code import Ui_InlineCodeEditor
from lang import translator

translate = QCoreApplication.translate


class InlineCodeEditor(QWidget):
    function = Tuple
    functions: Dict[str, List[function]] = None
    doc_items: List[List[QListWidgetItem]] = None

    submitted = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_InlineCodeEditor()

        translator.add(self.ui, self)
        self.ui.setupUi(self)

        if isinstance(parent, QLayout):
            parent.addWidget(self)

        self.ui.btnSubmit.clicked.connect(self.submitted.emit)
        self.ui.lstFuncs.itemDoubleClicked.connect(self.ins_func)

        self.load_funcs()

        self.ui.cbxFuncs.currentIndexChanged.connect(self.on_sel)
        self.ui.txtExpr.textChanged.connect(self.txt_changed)
        self.ui.btnClear.clicked.connect(self.clear)
        self.ui.btnClear.setVisible(False)

        self.on_sel(0)

    def get_text(self):
        return self.ui.txtExpr.text()

    def set_text(self, text: str):
        self.ui.txtExpr.setText(text)

    def on_sel(self, id: int):
        for idx, items in enumerate(self.doc_items):
            for it in items:
                it.setHidden(idx != id)

    def load_funcs(self):
        self.functions = maths.lib.get_funcs()
        self.doc_items = []
        for k in sorted(self.functions.keys()):
            self.ui.cbxFuncs.addItem(k)
            self.doc_items.append([])

            for f in sorted(self.functions[k], key=lambda x: x[0]):
                item_func = QListWidgetItem(self.ui.lstFuncs)
                w = QWidget()
                lay = QVBoxLayout()

                label_func = QLabel()
                label_func.setText(maths.lib.docs.get_func_def_html(f))

                lay.addWidget(label_func)

                label_desc = QLabel()
                desc = re.sub(r"{{(\w+)\}\}", "<i><b>\g<1></b></i>", html.escape(f[2]))
                desc = re.sub(r"//(\w+)//", "<i>\g<1></i>", desc)

                label_desc.setText(desc)

                label_desc.setAlignment(Qt.AlignRight)

                lay.addWidget(label_desc)
                lay.setSizeConstraint(QLayout.SetFixedSize)
                lay.setSpacing(2)
                lay.setContentsMargins(6, 6, 6, 6)
                w.setLayout(lay)
                item_func.setSizeHint(w.sizeHint())
                self.ui.lstFuncs.setItemWidget(item_func, w)
                self.doc_items[-1].append(item_func)
                item_func.setStatusTip(f[0])

    def ins_func(self, item: QListWidgetItem):
        self.set_text(self.get_text() + item.statusTip() + "()")

    def clear(self):
        self.set_text("")

    def txt_changed(self, txt: str):
        self.ui.btnClear.setVisible(bool(txt))
