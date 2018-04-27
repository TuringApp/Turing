# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from forms.ui_changtheme import Ui_ChangeThemeWindow
from util import theming
from util.widgets import center_widget

translate = QCoreApplication.translate

class ChangeThemeWindow(QDialog):
    def __init__(self, parent, orig=()):
        super().__init__(parent)
        self.ui = Ui_ChangeThemeWindow()
        self.ui.setupUi(self)
        self.setFixedWidth(self.width())
        self.adjustSize()
        self.setFixedSize(self.size())
        self.theme_callback = lambda: ()

        orig = orig or ("",) * 20

        def gen(txt):
            return lambda: self.change_color(txt)

        for i, t in enumerate(orig):
            txt = getattr(self.ui, "txtColor_%02d" % (i + 1))
            btn = getattr(self.ui, "btnCodeColor_%02d" % (i + 1))
            txt.setText(t)
            btn.clicked.connect(gen(txt))

        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_theme)

        center_widget(self, parent)


    def apply_theme(self):
        colors = [getattr(self.ui, "txtColor_%02d" % (i + 1)).text() for i in range(20)]
        theming.themes["custom"] = (theming.themes["custom"][0], colors)
        self.theme_callback()


    def done(self, res):
        if res == QDialog.Accepted:
            self.apply_theme()
            self.ok = True

        super(ChangeThemeWindow, self).done(res)


    def change_color(self, wgt):
        dlg = QColorDialog(self)
        dlg.setCurrentColor(QColor(wgt.text()))
        if dlg.exec_():
            wgt.setText(dlg.currentColor().name())


    def run(self):
        return self.exec_() == QDialog.Accepted and self.ok
