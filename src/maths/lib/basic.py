# -*- coding: utf-8 -*-

__desc__ = "Basic"

import builtins
import math
from .docs import *

doc("round", 
	[
		("num", "Number"), 
		("prec", "Integer", None, None)
	], 
	"Rounds {{num}} to the nearest integer / (if specified) to {{prec}} decimals.",
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
	"Returns the absolute value of {{num}}.")
def abs(x):
	return math.fabs(x)

doc("abs",
	[
		("num", "Number", ">= 0")
	],
	"Returns the square root of {{num}}.",
	["rac"])
def sqrt(x):
	return math.sqrt(x)

rac = sqrt

doc("root",
	[
		("num", "Number"),
		("n", "Number", "!= 0")
	],
	"Returns the {{n}}-th root of {{num}}.")
def root(x, n):
	return math.pow(x, 1 / n)

doc("pow",
	[
		("num", "Number"),
		("p", "Number")
	],
	"Returns {{num}} to the {{p}}-th power.",
	["puiss"])
def pow(x, y):
	return math.pow(x, y)

puiss = pow

doc("exp",
	[
		("num", "Number")
	],
	"Returns *e* to the power of {{num}}.")
def exp(x):
	return math.exp(x)

doc("ln",
	[
		("num", "Number")
	],
	"Returns the natural (base-*e*) logarithm of {{num}}.")
def ln(x):
	return math.log(x)

doc("log",
	[
		("num", "Number"),
		("b", "Number", "!= 0", 10)
	],
	"Returns the base-{{b}} logarithm of {{num}}.")
def log(x, b=10):
	return math.log(x, b)

doc("log10",
	[
		("num", "Number")
	],
	"Returns the base-10 logarithm of {{num}}.")
def log10(x):
	return math.log10(x)

doc("floor",
	[
		("num", "Number")
	],
	"Returns the largest integer less than or equal to {{num}}.")
def floor(x):
	return math.floor(x)

doc("ceil",
	[
		("num", "Number")
	],
	"Returns the smallest integer greater than or equal to {{num}}.")
def ceil(x):
	return math.ceil(x)

doc("sign",
	[
		("num", "Number")
	],
	"Returns the sign of {{num}} (-1 if negative, 1 if positive, 0 otherwise).")
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
	"Returns the greatest common divisor of {{a}} and {{b}}.",
	['pgcd'])
def gcd(a, b):
	return math.gcd(int(a), int(b))

pgcd = gcd

doc("lcm",
	[
		("a", "Integer"),
		("b", "Integer")
	],
	"Returns the least common multiple of {{a}} and {{b}}.",
	['ppcm'])
def lcm(a, b):
	return a * b / gcd(a, b)

ppcm = lcm