# -*- coding: utf-8 -*-

import builtins

def round(num, prec=None):
		if prec:
			return builtins.round(num, int(prec))
		return builtins.round(num)