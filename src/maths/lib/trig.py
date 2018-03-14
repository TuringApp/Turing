# -*- coding: utf-8 -*-

import math

def degrees(x):
	return math.degrees(x)

deg = degrees

def radians(x):
	return math.radians(x)

rad = radians

def asin(x):
	return math.asin(x)

def acos(x):
	return math.acos(x)

def atan(x):
	return math.atan(x)

def atan2(x, y):
	return math.atan2(x, y)

def asinh(x):
	return math.asinh(x)

def acosh(x):
	return math.acosh(x)

def atanh(x):
	return math.atanh(x)

def sin(x):
	return math.sin(x)

def cos(x):
	return math.cos(x)

def tan(x):
	return math.tan(x)

def sinh(x):
	return math.sinh(x)

def cosh(x):
	return math.cosh(x)

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