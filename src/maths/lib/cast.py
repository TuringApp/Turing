# -*- coding: utf-8 -*-

from .docs import doc

__desc__ = "Type conversion"

doc("c_bool",
	[
		("obj", "Any")
	],
	"Tries to convert {{obj}} to Boolean.")
def c_bool(obj):
	return bool(obj)

doc("c_num",
	[
		("obj", "Any")
	],
	"Tries to convert {{obj}} to Number.")
def c_num(obj):
	return float(obj)

doc("c_list",
	[
		("obj", "Any")
	],
	"Tries to convert {{obj}} to List.")
def c_list(obj):
	return list(obj)

doc("c_str",
	[
		("obj", "Any")
	],
	"Converts {{obj}} to String.")
def c_str(obj):
	if type(obj) == list:
		return "".join(obj)
	return str(obj)