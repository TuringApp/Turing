# -*- coding: utf-8 -*-

from ..util import math

def init_test():
	global test_results, test_stack, current_results
	test_results = []
	test_stack = []
	current_results = []

def begin_test(name):
	test_stack.append(name)
	print("[STAT] Beginning tests for: %s" % name)

def end_test(name):
	if test_stack[-1] != name:
		raise ValueError("Trying to pop the wrong value on the stack (got %s, expected %s)" % (name, test_stack[-1]))

	test_stack.pop()

	test_results.append((name, current_results))
	current_results.clear()
	print("[STAT] Ending tests for: %s" % name)

def expect(x, expec, info = ""):
	if isnum(x) and isnum(expec):
		val = isclose(x, expec)
	else:
		val = (x == expec)

	if val:
		stat = "PASSED"
		msg = "(value : '%s')" % str(x)
	else:
		stat = "FAILED"
		msg = "(expected: '%s', got: '%s')" % (str(expec), str(x))

	print("[TEST] #%02d : %s %s | %s" % (len(current_results) + 1, stat, msg, info))

	current_results.append((val, x, expec, info))