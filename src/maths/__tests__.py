# -*- coding: utf-8 -*-

from tests.framework import expect

from maths.parser import Parser
from maths.evaluator import Evaluator

tests = [
	("2+2", 4, "2 + 2"),
	("3*3", 9, "3 * 3"),
	("142        -9   ", 133, "142 - 9"),
	(" 50/10", 5, "50 / 10"),
	("72+  15", 87, "72 + 15"),
	(" 12*  4", 48, "12 * 4"),
	("4*2.5 + 8.5+1.5 / 3.0", 19, "4 * 2.5 + 8.5 + 1.5 / 3"),
	(" 2-7", -5, "2 - 7"),
	("2 -4 +6 -1 -1- 0 +8", 10, "2 - 4 + 6 - 1 - 1 - 0 + 8"),
	(" 2*3 - 4*5 + 6/3 ", -12, "2 * 3 - 4 * 5 + 6 / 3"),
	("10/4", 2.5, "10 / 4"),
	(" 2 - 1 + 14/0 + 7", float("inf"), "2 - 1 + 14 / 0 + 7"),

	("ceil(pi)", 4, "ceil(pi)"),
	("floor(e)", 2, "floor(e)"),
	("sqrt(49)", 7, "sqrt(49)"),
	("sqrt(2)^2", 2, "sqrt(2) ^ 2"),
	("cos(0)", 1, "cos(0)"),
	("sin(pi)", 0, "sin(pi)"),
	("deg(2pi)", 360, "deg(2 * pi)"),
	("round(asin(acos(atan(tan(cos(sin(0.5)))))),5)", 0.5, "round(asin(acos(atan(tan(cos(sin(0.5)))))), 5)"),

	("binomial(3,2)", 3, "binomial(3, 2)"),
	("binomial(3 , 0)", 1, "binomial(3, 0)"),

	("average(12,82,74,36,14,94)", 52, "average(12, 82, 74, 36, 14, 94)"),
	("sum(1,8,9,6,24,54,354)", 456, "sum(1, 8, 9, 6, 24, 54, 354)"),
    ("[8,5,42,96,31,84,35] [-4]", 96, "[8, 5, 42, 96, 31, 84, 35][-4]"),
    ("[1,2,3,4][2]", 3, "[1, 2, 3, 4][2]"),
    ("[42,{x,y,z}(x*abs({x, y}(x - y)(y, z))),38][1](4,3,5)", 8, "[42, {x, y, z}(x * abs({x, y}(x - y)(y, z))), 38][1](4, 3, 5)")
]

def run_tests():
	ev = Evaluator()

	for e, res, beaut in tests:
		ret = ev.evaluate(e)
		expect(ret, res)	
		expect(ev.beautified, beaut)
