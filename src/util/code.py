# -*- coding: utf-8 -*-
import re

from PyQt5.QtWidgets import QMessageBox

from maths.parser import Parser
from . import translate
from .widgets import get_themed_box, center_widget


def python_wrapper(input: str) -> str:
    return """# -*- coding: utf-8 -*-
import maths.lib
import types
for n, x in maths.lib.__dict__.items():
    if type(x) == types.ModuleType and "maths.lib." in x.__name__:
        module = __import__(x.__name__, globals(), locals(), ["*"], 0)
        for k, i in module.__dict__.items():
            if type(i) == types.FunctionType:
                globals()[k] = getattr(module, k)
            elif k.startswith("c_"):
                globals()[k[2:]] = getattr(module, k)
del maths, types, n, x

%s
""" % input


def try_parse(txt, parent=None):
    p = Parser(txt)

    ret = None

    try:
        ret = p.parse()
    except:
        ret = None

    msgs = p.log.get_messages()

    if msgs:
        box = get_themed_box()
        box.setIcon(QMessageBox.Critical)
        box.setStandardButtons(QMessageBox.Ok)
        box.setText(translate("Algo", "The following errors occured while parsing the expression:\n\n") + "\n".join(
            x[1] for x in msgs))
        box.adjustSize()
        center_widget(box, parent)
        box.exec_()
        ret = None

    return ret


def is_id(txt):
    return bool(re.search('^[a-zA-Z_0-9]+$', txt))
