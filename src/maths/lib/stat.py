# -*- coding: utf-8 -*-

import builtins
import math

def average(*args):
	"""Returns the average of a list."""
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args) / len(args)

moyenne = average

def sum(*args):
	"""Returns the sum of a list."""
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args)

def binomial(n, k):
	"""Calculates the binomial coefficient."""
	return math.gamma(n + 1) / (math.gamma(k + 1) * math.gamma(n - k + 1))

def max(lst):
	return max(lst)

def min(lst):
	return min(lst)

def gamma(x):
	return math.gamma(x)

def fact(x):
	return math.fact(x)

def erf(x):
	return math.erf(x)

def erfc(x):
	return math.erfc(x)

def map(func, lst):
	return list(builtins.map(func, lst))

appl = map

def filter(func, lst):
	return list(builtins.filter(func, lst))

filtre = filter