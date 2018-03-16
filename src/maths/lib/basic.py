# -*- coding: utf-8 -*-

import builtins
import math as rmath
from .docs import *
import cmath
import util

translate = util.translate

__desc__ = translate("Docs", "Basic")

doc("round",
    [
        ("num", "Real"),
        ("prec", "Integer", None, None)
    ],
    translate("Docs", "Rounds {{num}} to the nearest integer / (if specified) to {{prec}} decimals."),
    ["arrondi"])


def round(num, prec=None):
    if prec:
        return builtins.round(num, int(prec))
    return builtins.round(num)


arrondi = round

doc("abs",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the absolute value of {{num}}."))


def abs(x):
    return builtins.abs(x)


doc("sqrt",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the square root of {{num}}. If {{num}} < 0, the result will be Complex."),
    ["rac"])


def sqrt(x):
    return cmath.sqrt(x)


rac = sqrt

doc("root",
    [
        ("num", "Number"),
        ("n", "Number", "!= 0")
    ],
    translate("Docs", "Returns the {{n}}-th root of {{num}}."))


def root(x, n):
    return pow(x, 1 / n)


doc("pow",
    [
        ("num", "Number"),
        ("p", "Number")
    ],
    translate("Docs", "Returns {{num}} to the {{p}}-th power."),
    ["puiss"])


def pow(x, y):
    return x ** y


puiss = pow

doc("exp",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns //e// to the power of {{num}}."))


def exp(x):
    return cmath.exp(x)


doc("ln",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the natural (base-//e//) logarithm of {{num}}."))


def ln(x):
    return cmath.log(x)


doc("log",
    [
        ("num", "Number"),
        ("b", "Number", "!= 0", 10)
    ],
    translate("Docs", "Returns the base-{{b}} logarithm of {{num}}."))


def log(x, b=10):
    return cmath.log(x, b)


doc("log10",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the base-10 logarithm of {{num}}."))


def log10(x):
    return cmath.log10(x)


doc("floor",
    [
        ("num", "Real")
    ],
    translate("Docs", "Returns the largest integer less than or equal to {{num}}."))


def floor(x):
    return rmath.floor(x)


doc("ceil",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the smallest integer greater than or equal to {{num}}."))


def ceil(x):
    return rmath.ceil(x)


doc("sign",
    [
        ("num", "Real")
    ],
    translate("Docs", "Returns the sign of {{num}} (-1 if negative, 1 if positive, 0 otherwise)."))


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


doc("gcd",
    [
        ("a", "Integer"),
        ("b", "Integer")
    ],
    translate("Docs", "Returns the greatest common divisor of {{a}} and {{b}}."),
    ['pgcd'])


def gcd(a, b):
    return rmath.gcd(int(a), int(b))


pgcd = gcd

doc("lcm",
    [
        ("a", "Integer"),
        ("b", "Integer")
    ],
    translate("Docs", "Returns the least common multiple of {{a}} and {{b}}."),
    ['ppcm'])


def lcm(a, b):
    return a * b / gcd(a, b)


ppcm = lcm

doc("arg",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the argument (or phase) of {{x}}."),
    ["phase"])


def arg(x):
    return cmath.phase(x)


phase = arg

doc("polar",
    [
        ("x", "Number")
    ],
    translate("Docs",
              "Returns a list containing the polar coordinates of {{x}}, respectively the modulus (radius) and argument (angle)."),
    ["polaire"])


def polar(x):
    return [abs(x), arg(x)]


polaire = polar

doc("rect",
    [
        ("r", "Number"),
        ("phi", "Number")
    ],
    translate("Docs", "Converts the specified polar coordinates to a complex number."))


def rect(r, phi):
    return r * exp(phi * 1j)
