# -*- coding: utf-8 -*-

__desc__ = "Trigonometry"

import math
from .docs import *

doc_c("pi", "π", "Perimeter of a circle of diameter 1")
c_pi = 3.14159265358979323846264338327950288419716939937511

doc_c("tau", "τ", "Double of π")
c_tau = 6.28318530717958647692528676655900576839433879875021

doc("degrees",
	[
		("x", "Number")
	],
	"Converts angle {{x}} from radians to degrees.",
	["deg"])
def degrees(x):
	return math.degrees(x)

deg = degrees

doc("radians",
	[
		("x", "Number")
	],
	"Converts angle {{x}} from degrees to radians.",
	["rad"])
def radians(x):
	return math.radians(x)

rad = radians

doc("asin", [("x", "Number")], "Returns the arc sine of {{x}}.")
def asin(x):
	return math.asin(x)

doc("acos", [("x", "Number")], "Returns the arc cosine of {{x}}.")
def acos(x):
	return math.acos(x)

doc("atan", [("x", "Number")], "Returns the arc tangent of {{x}}.")
def atan(x):
	return math.atan(x)

doc("atan2", [("x", "Number"), ("y", "Number")], "Returns the arc tangent of {{y}} / {{x}}.")
def atan2(x, y):
	return math.atan2(x, y)

doc("asinh", [("x", "Number")], "Returns the inverse hyperbolic sine of {{x}}.")
def asinh(x):
	return math.asinh(x)

doc("acosh", [("x", "Number")], "Returns the inverse hyperbolic cosine of {{x}}.")
def acosh(x):
	return math.acosh(x)

doc("atanh", [("x", "Number")], "Returns the inverse hyperbolic tangent of {{x}}.")
def atanh(x):
	return math.atanh(x)

doc("sin", [("x", "Number")], "Returns the sine of {{x}}.")
def sin(x):
	return math.sin(x)

doc("cos", [("x", "Number")], "Returns the cosine of {{x}}.")
def cos(x):
	return math.cos(x)

doc("tan", [("x", "Number")], "Returns the tangent of {{x}}.")
def tan(x):
	return math.tan(x)

doc("sinh", [("x", "Number")], "Returns the hyperbolic sine of {{x}}.")
def sinh(x):
	return math.sinh(x)

doc("cosh", [("x", "Number")], "Returns the hyperbolic cosine of {{x}}.")
def cosh(x):
	return math.cosh(x)

doc("tanh", [("x", "Number")], "Returns the hyperbolic tangent of {{x}}.")
def tanh(x):
	return math.tanh(x)

def sec(x):
	return 1 / cos(x)

def csc(x):
	return 1 / sin(x)

def cot(x):
	return 1 / tan(x)

def exsec(x):
	return sec(x) - 1

def excsc(x):
	return csc(x) - 1

def chord(x):
	return 2 * sin(x / 2)

def sech(x):
	return 1 / cosh(x)

def csch(x):
	return 1 / sinh(x)

def coth(x):
	return 1 / tanh(x) 

def asec(x):
	return acos(1 / x)

def acsc(x):
	return asin(1 / x)

def acot(x):
	return atan(1 / x)

def asech(x):
	return acosh(1 / x)

def acsch(x):
	return asinh(1 / x)

def acoth(x):
	return atanh(1 / x)

def sinc(x):
	return sin(x) / x

def versin(x):
	return 1 - cos(x)

def vercos(x):
	return 1 + cos(x)

def coversin(x):
	return 1 - sin(x)

def covercos(x):
	return 1 + sin(x)

def haversin(x):
	return versin(x) / 2

def havercos(x):
	return vercos(x) / 2

def hacoversin(x):
	return coversin(x) / 2

def hacovercos(x):
	return covercos(x) / 2

def hypot(x, y):
	return math.hypot(x, y)