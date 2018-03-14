# -*- coding: utf-8 -*-

__desc__ = "Statistics"

import builtins
import math
from .docs import *

doc_c("catalan", "G", "Catalan's constant")
c_catalan = 0.91596559417721901505460351493238411077414937428167

doc_c("glaisher", "A", "Glaisher-Kinkelin constant")
c_glaisher = 1.28242712910062263687534256886979172776768892732500

doc("average",
	[
		("args", "List(Number) / Number*")
	],
	"Returns the arithmetic mean of {{args}}.",
	["moyenne"])
def average(*args):
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args) / len(args)

moyenne = average

doc("sum",
	[
		("args", "List(Number) / Number*")
	],
	"Returns the sum of all the terms of {{args}}.")
def sum(*args):
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args)

doc("binomial",
	[
		("n", "Number"),
		("k", "Number")
	],
	"Returns the binomial coefficient for a subset of size {{k}} and a set of size {{n}}.")
def binomial(n, k):
	"""Calculates the binomial coefficient."""
	return math.gamma(n + 1) / (math.gamma(k + 1) * math.gamma(n - k + 1))

doc("max",
	[
		("args", "List(Number) / Number*")
	],
	"Returns the maximum value of {{args}}.")
def max(*args):
	if type(args[0]) == list:
		args = args[0]

	return builtins.max(args)

doc("min",
	[
		("args", "List(Number) / Number*")
	],
	"Returns the minimum value of {{args}}.")
def min(*args):
	if type(args[0]) == list:
		args = args[0]

	return builtins.min(args)

doc("gamma",
	[
		("x", "Number")
	],
	"Returns the Gamma function at {{x}}.")
def gamma(x):
	return math.gamma(x)

doc("fact",
	[
		("x", "Integer")
	],
	"Returns the factorial of {{x}}.")
def fact(x):
	return math.fact(x)

doc("erf",
	[
		("x", "Number")
	],
	"Returns the error function at {{x}}.")
def erf(x):
	return math.erf(x)

doc("erfc",
	[
		("x", "Number")
	],
	"Returns the complementary error function at {{x}}.")
def erfc(x):
	return math.erfc(x)

doc("map",
	[
		("func", "Function(1 arg)"),
		("lst", "List")
	],
	"Applies {{func}} to each element of {{lst}} and returns the resulting list.",
	["appl"])
def map(func, lst):
	return list(builtins.map(func, lst))

appl = map

doc("filter",
	[
		("func", "Function(1 arg)"),
		("lst", "List")
	],
	"Returns a list containing all elements of {{lst}} for which {{func}} returns a truthy value.",
	["filtre"])
def filter(func, lst):
	return list(builtins.filter(func, lst))

filtre = filter