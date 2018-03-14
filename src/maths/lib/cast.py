# -*- coding: utf-8 -*-

def c_bool(obj):
	return bool(obj)

def c_num(obj):
	return float(obj)

def c_list(obj):
	return list(obj)

def c_str(obj):
	if type(obj) == list:
		return "".join(obj)
	return str(obj)