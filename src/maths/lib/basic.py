# -*- coding: utf-8 -*-

import builtins
import cmath
import math as rmath

import util
from .docs import *

translate = util.translate

__desc__ = translate("Docs", "Basic")

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
        ("num", "Number")
    ],
    translate("Docs", "Returns the largest integer less than or equal to {{num}}."))


def floor(x):
    if type(x) == complex:
        return complex(rmath.floor(x.real), rmath.floor(x.imag))
    return rmath.floor(x)


doc("ceil",
    [
        ("num", "Number")
    ],
    translate("Docs", "Returns the smallest integer greater than or equal to {{num}}."))


def ceil(x):
    if type(x) == complex:
        return complex(rmath.ceil(x.real), rmath.ceil(x.imag))
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
              "Returns a list containing the polar coordinates of {{x}}, respectively the modulus (radius) "
              "and argument (angle)."),
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


doc("re",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the real part of {{x}}."))


def re(x):
    return complex(x).real


doc("im",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the imaginary part of {{x}}."))


def im(x):
    return complex(x).imag


doc("conj",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the complex conjugate of {{x}}."))


def conj(x):
    return complex(x).conjugate()


doc("gradient",
    [
        ("func", "Function(Number)"),
        ("x", "Number"),
        ("h", "Number", None, 1e-7)
    ],
    translate("Docs", "Returns the gradient of {{func}} at {{x}} (optional precision {{h}})."))


def gradient(func, x, h=1e-7):
    result = (func(x + h) - func(x - h)) / (2 * h)
    if h < 1:
        result = round(result, -int(round(log10(h).real)))
    return result


doc("derivative",
    [
        ("func", "Function(Number)"),
        ("h", "Number", None, 1e-7)
    ],
    translate("Docs", "Returns the derivative of {{func}} (optional precision {{h}})."),
    ["deriv"])


def derivative(func, h=1e-7):
    return lambda x: gradient(func, x, h)


deriv = derivative

doc("integrate",
    [
        ("func", "Function(Number)"),
        ("a", "Number"),
        ("b", "Number"),
        ("steps", "Integer", None, 100000)
    ],
    translate("Docs", "Returns the integral of {{func}} from {{a}} to {{b}} (optional number of steps: {{steps}})."),
    ["integ"])


def integrate(func, a, b, steps=1000):
    step = (b - a) / steps

    sum = func(a)

    for i in range(1, steps, 2):
        sum += 4 * func(a + step * i)

    for i in range(2, steps - 1, 2):
        sum += 2 * func(a + step * i)

    sum += func(b)

    return sum * step / 3


integ = integrate
