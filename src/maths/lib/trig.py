# -*- coding: utf-8 -*-

import cmath

from maths.lib import basic
from util import translate
from .docs import *

__desc__ = translate("Docs", "Trigonometry")

doc_c("pi", "π", "Perimeter of a circle of diameter 1")
c_pi = 3.14159265358979323846264338327950288419716939937511

doc_c("tau", "τ", "Double of π")
c_tau = 6.28318530717958647692528676655900576839433879875021

deg_cst = 180 / c_pi
rad_cst = c_pi / 180

doc("degrees",
    [
        ("x", "Number")
    ],
    translate("Docs", "Converts angle {{x}} from radians to degrees."),
    ["deg"])


def degrees(x):
    return x * deg_cst


deg = degrees

doc("radians",
    [
        ("x", "Number")
    ],
    translate("Docs", "Converts angle {{x}} from degrees to radians."),
    ["rad"])


def radians(x):
    return x * rad_cst


rad = radians

doc("asin", [("x", "Number")], translate("Docs", "Returns the arc sine of {{x}}."))


def asin(x):
    return cmath.asin(x)


doc("acos", [("x", "Number")], translate("Docs", "Returns the arc cosine of {{x}}."))


def acos(x):
    return cmath.acos(x)


doc("atan", [("x", "Number")], translate("Docs", "Returns the arc tangent of {{x}}."))


def atan(x):
    return cmath.atan(x)


doc("atan2", [("y", "Number"), ("x", "Number")], translate("Docs", "Returns the arc tangent of {{y}} / {{x}}."))


def atan2(y, x):
    return atan(y / x)


doc("asinh", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic sine of {{x}}."))


def asinh(x):
    return cmath.asinh(x)


doc("acosh", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic cosine of {{x}}."))


def acosh(x):
    return cmath.acosh(x)


doc("atanh", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic tangent of {{x}}."))


def atanh(x):
    return cmath.atanh(x)


doc("sin", [("x", "Number")], translate("Docs", "Returns the sine of {{x}}."))


def sin(x):
    return cmath.sin(x)


doc("cos", [("x", "Number")], translate("Docs", "Returns the cosine of {{x}}."))


def cos(x):
    return cmath.cos(x)


doc("tan", [("x", "Number")], translate("Docs", "Returns the tangent of {{x}}."))


def tan(x):
    return cmath.tan(x)


doc("sinh", [("x", "Number")], translate("Docs", "Returns the hyperbolic sine of {{x}}."))


def sinh(x):
    return cmath.sinh(x)


doc("cosh", [("x", "Number")], translate("Docs", "Returns the hyperbolic cosine of {{x}}."))


def cosh(x):
    return cmath.cosh(x)


doc("tanh", [("x", "Number")], translate("Docs", "Returns the hyperbolic tangent of {{x}}."))


def tanh(x):
    return cmath.tanh(x)


doc("sec", [("x", "Number")], translate("Docs", "Returns the secant of {{x}}."))


def sec(x):
    return 1 / cos(x)


doc("csc", [("x", "Number")], translate("Docs", "Returns the cosecant of {{x}}."))


def csc(x):
    return 1 / sin(x)


doc("cot", [("x", "Number")], translate("Docs", "Returns the cotangent of {{x}}."))


def cot(x):
    return 1 / tan(x)


doc("exsec", [("x", "Number")], translate("Docs", "Returns the exsecant of {{x}}."))


def exsec(x):
    return sec(x) - 1


doc("excsc", [("x", "Number")], translate("Docs", "Returns the excosecant of {{x}}."))


def excsc(x):
    return csc(x) - 1


doc("chord", [("x", "Number")], translate("Docs", "Returns the chord of {{x}}."), ["crd"])


def chord(x):
    return 2 * sin(x / 2)


crd = chord

doc("sech", [("x", "Number")], translate("Docs", "Returns the hyperbolic secant of {{x}}."))


def sech(x):
    return 1 / cosh(x)


doc("csch", [("x", "Number")], translate("Docs", "Returns the hyperbolic cosecant of {{x}}."))


def csch(x):
    return 1 / sinh(x)


doc("coth", [("x", "Number")], translate("Docs", "Returns the hyperbolic cotangent of {{x}}."))


def coth(x):
    return 1 / tanh(x)


doc("asec", [("x", "Number")], translate("Docs", "Returns the inverse secant of {{x}}."))


def asec(x):
    return acos(1 / x)


doc("acsc", [("x", "Number")], translate("Docs", "Returns the inverse cosecant of {{x}}."))


def acsc(x):
    return asin(1 / x)


doc("acot", [("x", "Number")], translate("Docs", "Returns the inverse cotangent of {{x}}."))


def acot(x):
    return atan(1 / x)


doc("asech", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic secant of {{x}}."))


def asech(x):
    return acosh(1 / x)


doc("acsch", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic cosecant of {{x}}."))


def acsch(x):
    return asinh(1 / x)


doc("acoth", [("x", "Number")], translate("Docs", "Returns the inverse hyperbolic cotangent of {{x}}."))


def acoth(x):
    return atanh(1 / x)


doc("sinc", [("x", "Number")], translate("Docs", "Returns the cardinal sine of {{x}}."))


def sinc(x):
    return sin(x) / x


doc("versin", [("x", "Number")], translate("Docs", "Returns the versed sine of {{x}}."))


def versin(x):
    return 1 - cos(x)


doc("vercos", [("x", "Number")], translate("Docs", "Returns the versed cosine of {{x}}."))


def vercos(x):
    return 1 + cos(x)


doc("coversin", [("x", "Number")], translate("Docs", "Returns the coversed sine of {{x}}."))


def coversin(x):
    return 1 - sin(x)


doc("covercos", [("x", "Number")], translate("Docs", "Returns the coversed cosine of {{x}}."))


def covercos(x):
    return 1 + sin(x)


doc("coversin", [("x", "Number")], translate("Docs", "Returns the haversed sine of {{x}}."))


def haversin(x):
    return versin(x) / 2


doc("havercos", [("x", "Number")], translate("Docs", "Returns the haversed cosine of {{x}}."))


def havercos(x):
    return vercos(x) / 2


doc("hacoversin", [("x", "Number")], translate("Docs", "Returns the hacoversed sine of {{x}}."))


def hacoversin(x):
    return coversin(x) / 2


doc("hacovercos", [("x", "Number")], translate("Docs", "Returns the hacoversed cosine of {{x}}."))


def hacovercos(x):
    return covercos(x) / 2


doc("hypot", [("x", "Number"), ("y", "Number")],
    translate("Docs", "Returns the hypotenuse / Euclidean norm of the vector ({{x}}, {{y}})."))


def hypot(x, y):
    return basic.sqrt(basic.pow(x, 2) + basic.pow(y, 2))
