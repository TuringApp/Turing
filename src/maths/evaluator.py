# -*- coding: utf-8 -*-

from maths.parser import *
import math
import random
from util.math import isclose, isnum
import maths.lib as mlib
import maths.nodes as nodes
from util.log import Logger
import sys

class Evaluator:
	variables = None
	arguments = None
	log = None
	beautified = None

	def round_ex(num, prec=None):
		if prec:
			return round(num, int(prec))
		return round(num)

	def __init__(self):
		self.variables = {
			"pi": math.pi,
			"e": math.e,

			"sqrt": math.sqrt,
            "racine": math.sqrt,
			"pow": math.pow,
            "puiss": math.pow,

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
            "arrondi": mlib.round,
			
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

			"sum": mlib.sum,
			"average": mlib.average,
            "moyenne": mlib.average,
			"max": max,
			"min": min
		}
		self.arguments = []
		self.log = Logger("Eval")

	def evaluate(self, expr):
		par = Parser(expr)
		exp = None

		if False:
			exp = par.parse()
		else:
			try:
				exp = par.parse()
			except:
				self.log.error("Parser: " + str(sys.exc_info()[1]))

		for msg in par.log.getMessages():
			self.log.messages.append(msg)

		self.beautified = par.beautify()

		if not exp:
			return None

		ret = None

		try:
			ret = self.evalNode(exp)
		except:
			self.log.error(str(sys.exc_info()[1]))

		return ret

	def evalNode(self, node):
		val = self.evalNodeReal(node)

		if val != None and isnum(val) and not isinstance(val, bool):
			val = round(val, 9)
			if isclose(val, 0):
				val = 0

		return val

	def callLambda(self, node, *args):
		args = list(args)
		if len(args) != len(node.args):
			self.log.error("Argument count mismatch (expected %d, got %d)" % (len(node.args), len(args)))
		for i in range(len(args)):
			self.arguments.append((node.args[i], args[i]))
		ret = self.evalNode(node.expr)
		for i in range(len(args)):
			self.arguments.pop()	
		return ret

	def evalNodeReal(self, node):
		if type(node) in [nodes.NumberNode, nodes.StringNode, nodes.ListNode]:
			return node.value

		if type(node) == nodes.IdentifierNode:
			for a in self.arguments[::-1]:
				if a[0] == node.value:
					return a[1]
			if node.value in self.variables:
				return self.variables[node.value]
			else:
				self.log.error("Can't find variable or function " + node.value)

		if type(node) == nodes.UnaryOpNode:
			return self.evalUnary(node)

		if type(node) == nodes.BinOpNode:
			return self.evalBinary(node)

		if type(node) == nodes.CallNode:
			fn = self.evalNode(node.func)
			args = [self.evalNode(x) for x in node.args]
			return fn.__call__(*args)
			if node.func in self.functions:
				args = [self.evalNode(x) for x in node.args]
				return self.functions[node.func](*args)
			else:
				self.log.error("Unknown function '%s'" % node.func)

		if type(node) == nodes.ArrayAccessNode:
			val = self.evalNode(node.array)
			idx = int(self.evalNode(node.index))
			if idx < len(val):
				return self.evalNode(val[idx])
			else:
				self.log.error("Index '%s' too big for array" % idx)

		if type(node) == nodes.LambdaNode:
			return lambda *args: self.callLambda(node, *list(args))

		if not isinstance(node, nodes.AstNode):
			return node

		return None

	def evalUnary(self, node):
		val = self.evalNode(node.value)

		if node.opType == "-":
			return -val

		if node.opType == "NON":
			return not val

		self.log.error("Invalid unary operator '%s'" % node.opType)

	def evalBinary(self, node):
		left = self.evalNode(node.left)
		right = self.evalNode(node.right)

		if left == None or right == None:
			self.log.error("Trying to use None")
			return None

		if node.opType == "+": return left + right
		if node.opType == "-": return left - right
		if node.opType == "*": return left * right
		if node.opType == "/": return float("inf") if isclose(right, 0) else left / right
		if node.opType == "%": return math.fmod(left, right)
		if node.opType == "^": return left ** right

		if node.opType == "==": return isclose(left, right)
		if node.opType == "!=": return not isclose(left, right)
		if node.opType == "<=": return left <= right or isclose(left, right)
		if node.opType == "< ": return left <  right
		if node.opType == "> ": return left >  right
		if node.opType == ">=": return left >= right or isclose(left, right)

		if node.opType == "&": return int(left) & int(right)
		if node.opType == "|": return int(left) | int(right)
		if node.opType == "XOR": return int(left) ^ int(right)

		self.log.error("Invalid binary operator '%s'" % node.opType)
