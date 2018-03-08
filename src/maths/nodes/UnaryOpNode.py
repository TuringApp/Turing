# -*- coding: utf-8 -*-

from .AstNode import *

class UnaryOpNode(AstNode):
	"""Unary operator node

	value  -- value (AstNode)
	opType -- which unary operator (str)"""
	value = None
	opType = None

	def __init__(self, value, opType):
		self.value = value
		self.opType = opType

	def __str__(self):
		return "[UnaryOp %s (%s)]" % (self.opType, self.value)

	def __repr__(self):
		return "UnaryOpNode(%r, %r)" % (self.value, self.opType)