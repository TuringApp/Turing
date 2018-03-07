# -*- coding: utf-8 -*-

import numbers

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return (a == b) or abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def isnum(a):
	return isinstance(a, numbers.Number)