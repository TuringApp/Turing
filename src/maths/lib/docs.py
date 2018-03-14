# -*- coding: utf-8 -*-

import inspect

funcs = {}

def doc(*kwargs):
	module = inspect.getmodule(inspect.stack()[1][0])
	mod_name = module.__desc__
	if mod_name not in funcs:
		funcs[mod_name] = []
	funcs[mod_name].append(kwargs)
