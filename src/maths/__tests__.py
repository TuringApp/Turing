# -*- coding: utf-8 -*-

from tests.framework import expect

from maths.parser import Parser
from maths.evaluator import Evaluator

tests = [
	("2+2", 4),
	("3*3", 9),
	("142        -9   ", 133),
	(" 50/10", 5),
	("72+  15", 87),
	(" 12*  4", 48),
	("4*2.5 + 8.5+1.5 / 3.0", 19),
	(" 2-7", -5),
	("2 -4 +6 -1 -1- 0 +8", 10),
	(" 2*3 - 4*5 + 6/3 ", -12),
	("10/4", 2.5),
	(" 2 - 1 + 14/0 + 7", float("inf")),

	("ceil(pi)", 4),
	("floor(e)", 2),
	("sqrt(49)", 7),
	("sqrt(2)^2", 2),
	("cos(0)", 1),
	("sin(pi)", 0),
	("deg(2pi)", 360),
	("round(asin(acos(atan(tan(cos(sin(0.5)))))),5)", 0.5),

	("binomial(3, 2)", 3),
	("binomial(3, 0)", 1),

	("average(12, 82, 74, 36, 14, 94)", 52),
	("sum(1, 8, 9, 6, 24, 54, 354)", 456)
]

def run_tests():
	ev = Evaluator()

	for e, r in tests:
		ret = ev.evaluate(e)
		expect(ret, r)	