# -*- coding: utf-8 -*-

import util
from .docs import *

from util import translate

__desc__ = translate("Docs", "Type conversion")

doc("c_bool",
    [
        ("obj", "Any")
    ],
    translate("Docs", "Tries to convert {{obj}} to Boolean."))


def c_bool(obj):
    return bool(obj)


doc("c_num",
    [
        ("obj", "Any")
    ],
    translate("Docs", "Tries to convert {{obj}} to Number."))


def c_num(obj):
    return complex(obj)


doc("c_list",
    [
        ("obj", "Any")
    ],
    translate("Docs", "Tries to convert {{obj}} to List."))


def c_list(obj):
    return list(obj)


doc("c_str",
    [
        ("obj", "Any")
    ],
    translate("Docs", "Converts {{obj}} to String."))


def c_str(obj):
    if type(obj) == list:
        return "".join(obj)
    return str(obj)
