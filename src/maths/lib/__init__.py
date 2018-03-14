# -*- coding: utf-8 -*-

import types

import maths.lib.basic
import maths.lib.cast
import maths.lib.geom
import maths.lib.stats
import maths.lib.trig
import maths.lib.const
import maths.lib.physics

def get_funcs():
	import maths.lib.docs
	return docs.funcs

def get_consts():
	import maths.lib.docs
	return docs.consts

def get_modules():
	import maths.lib.docs
	return docs.modules