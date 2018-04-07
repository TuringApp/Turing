# -*- coding: utf-8 -*-


from util import translate
from .docs import *

__desc__ = translate("Docs", "Algobox compatibility")

doc("round",
    [
        ("num", "Number"),
        ("prec", "Integer", None, None)
    ],
    translate("Docs", "Rounds {{num}} to the nearest integer / (if specified) to {{prec}} decimals."),
    ["arrondi"])


def round(num, prec=None):
    if type(num) == complex:
        return complex(round(num.real, prec), round(num.imag, prec))
    if prec:
        return builtins.round(num, int(prec))
    return builtins.round(num)
