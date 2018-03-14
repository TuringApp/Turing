# -*- coding: utf-8 -*-

import builtins
import math

def round(num, prec=None):
		if prec:
			return builtins.round(num, int(prec))
		return builtins.round(num)

arrondi = round

def abs(x):
	return math.fabs(x)

def sqrt(x):
	return math.sqrt(x)

rac = sqrt

def root(x, n):
	return math.pow(x, 1 / n)

def pow(x):
	return math.pow(x)

puiss = pow

def exp(x):
	return math.exp(x)

def ln(x):
	return math.log(x)

def log(x, b=10):
	return math.log(x, b)

def log10(x):
	return math.log10(x)

def floor(x):
	return math.floor(x)

def ceil(x):
	return math.ceil(x)

def sign(x):
	if x < 0:
		return -1
	if x > 0:
		return 1
	return 0

def gcd(a, b):
	return math.gcd

pgcd = gcd