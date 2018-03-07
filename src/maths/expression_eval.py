# -*- coding: utf-8 -*-

from maths.expression import *
import math
import random
from util.math import isclose, isnum

def error(msg):
	print(msg)

class ExprEvaluator:
	variables = None
	functions = None

	def round_ex(num, prec=None):
		if prec:
			return round(num, int(prec))
		return round(num)

	def __init__(self):
		self.variables = {
			"pi": math.pi,
			"e": math.e
		}
		self.functions = {
			"sqrt": math.sqrt,
			"pow": math.pow,

			"cos": math.cos,
			"sin": math.sin,
			"tan": math.tan,
			"acos": math.acos,
			"asin": math.asin,
			"atan": math.atan,
			"atan2": math.atan2,

			"cosh": math.cosh,
			"sinh": math.sinh,
			"tanh": math.tanh,
			"acosh": math.acosh,
			"asinh": math.asinh,
			"atanh": math.atanh,

			"deg": math.degrees,
			"rad": math.radians,

			"exp": math.exp,
			"ln": math.log,
			"log": math.log,
			"log10": math.log10,

			"abs": math.fabs,
			"floor": math.floor,
			"ceil": math.ceil,
			"round": ExprEvaluator.round_ex,
			
			"random": random.random,
			"fact": math.factorial,
			"gamma": math.gamma
		}



	def evaluate(self, expr):
		par = Parser(expr)
		exp = par.parse()
		return self.evalNode(exp)

	def evalNode(self, node):
		val = self.evalNodeReal(node)
		if val:
			val = round(val, 9)
			if isclose(val, 0):
				val = 0
		return val

	def evalNodeReal(self, node):
		if type(node) in [NumberNode, StringNode]:
			return node.value

		if type(node) == IdentifierNode:
			if node.value in self.variables:
				return self.variables[node.value]
			else:
				error("Can't find variable " + node.value)

		if type(node) == UnaryOpNode:
			return self.evalUnary(node)

		if type(node) == OPERATORNode:
			return self.evalBinary(node)

		if type(node) == CallNode:
			if node.func in self.functions:
				args = [self.evalNode(x) for x in node.args]
				return self.functions[node.func](*args)
			else:
				error("Unknown function")


		error("Shit brixes")

	def evalUnary(self, node):
		val = self.evalNode(node.value)

		if node.opType == "-":
			return -val

		if node.opType == "NON":
			return not val

		error("Shit brixes")

	def evalBinary(self, node):
		left = self.evalNode(node.left)
		right = self.evalNode(node.right)

		if node.opType == "+": return left + right
		if node.opType == "-": return left - right
		if node.opType == "*": return left * right
		if node.opType == "/": return float("inf") if isclose(right, 0) else left / right
		if node.opType == "%": return math.fmod(left, right)
		if node.opType == "^": return left ** right

		if node.opType == "==": return utils.isclose(left, right)
		if node.opType == "!=": return not utils.isclose(left, right)
		if node.opType == "<=": return left <= right or utils.isclose(left, right)
		if node.opType == "< ": return left <  right
		if node.opType == "> ": return left >  right
		if node.opType == ">=": return left >= right or utils.isclose(left, right)

		if node.opType == "ET": return left and right
		if node.opType == "OU": return left or right
		if node.opType == "XOR": return left ^ right

		error("Shit brixes")