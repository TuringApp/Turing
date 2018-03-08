# -*- coding: utf-8 -*-

from maths.parser import *
import math
import random
from util.math import isclose, isnum
import maths.lib as mlib

def error(msg):
	print(msg)

class Evaluator:
	variables = None
	functions = None
	arguments = None

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
			"round": mlib.round,
			
			"random": random.random,
			"randint": random.randint,
			"uniform": random.uniform,
			"distrib_beta": random.betavariate,
			"distrib_expo": random.expovariate,
			"distrib_gamma": random.gammavariate,
			"distrib_gauss": random.gauss,
			"distrib_lognorm": random.lognormvariate,
			"distrib_normal": random.normalvariate,
			"distrib_pareto": random.paretovariate,
			"distrib_weibull": random.weibullvariate,

			"fact": math.factorial,
			"gamma": math.gamma,
			"binomial": mlib.binomial,

			"list": mlib.genlist,
			"sum": mlib.sum,
			"average": mlib.average,
			"max": max,
			"min": min
		}
		self.arguments = []

	def evaluate(self, expr):
		par = Parser(expr)
		exp = par.parse()
		return self.evalNode(exp)

	def evalNode(self, node):
		val = self.evalNodeReal(node)
		if val and isnum(val):
			val = round(val, 9)
			if isclose(val, 0):
				val = 0
		return val

	def evalNodeReal(self, node):
		if type(node) in [NumberNode, StringNode, ListNode]:
			return node.value

		if type(node) == IdentifierNode:
			for a in self.arguments[::-1]:
				if a[0] == node.value:
					return a[1]
			if node.value in self.variables:
				return self.variables[node.value]
			else:
				error("Can't find variable " + node.value)

		if type(node) == UnaryOpNode:
			return self.evalUnary(node)

		if type(node) == BinOpNode:
			return self.evalBinary(node)

		if type(node) == CallNode:
			if node.func in self.functions:
				args = [self.evalNode(x) for x in node.args]
				return self.functions[node.func](*args)
			else:
				error("Unknown function '%s'" % node.func)

		if type(node) == ArrayAccessNode:
			val = self.evalNode(node.array)
			idx = int(self.evalNode(node.index))
			if idx < len(val):
				return self.evalNode(val[idx])
			else:
				error("Index '%s' too big for array" % idx)

		if not isinstance(node, AstNode):
			return node

		return None

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

		if node.opType == "&": return int(left) and int(right)
		if node.opType == "|": return int(left) or int(right)
		if node.opType == "XOR": return int(left) ^ int(right)

		error("Shit brixes")
