# -*- coding: utf-8 -*-

import builtins
import math

def average(*args):
	"""Returns the average of a list."""
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args) / len(args)

def sum(*args):
	"""Returns the sum of a list."""
	if type(args[0]) == list:
		args = args[0]
	
	return builtins.sum(args)

def binomial(n, k):
	"""Calculates the binomial coefficient."""
	return math.gamma(n + 1) / (math.gamma(k + 1) * math.gamma(n - k + 1))