# -*- coding: utf-8 -*-

"""
Mathematical functions library.

For the ones not already present in Python's math.
"""

import builtins
import math

def round(num, prec=None):
		if prec:
			return builtins.round(num, int(prec))
		return builtins.round(num)

def binomial(n, k):
	"""Calculates the binomial coefficient."""
	return math.gamma(n + 1) / (math.gamma(k + 1) * math.gamma(n - k + 1))

def genlist(*args):
	"""Helper function. Generates a list from arguments."""
	return list(args)

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
