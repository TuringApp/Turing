# -*- coding: utf-8 -*-

from .AstNode import *

class BinOpNode(AstNode):
	"""Binary (two operands) operator node

	left   -- left operand (AstNode)
	right  -- right operand (AstNode)
	opType -- which binary operator (str)"""
	left = None
	right = None
	opType = None

	def __init__(self, left, right, opType):
		self.left = left
		self.right = right
		self.opType = opType

	def __str__(self):
		return "[BinOp (%s) %s (%s)]" % (self.left, self.opType, self.right)

	def __repr__(self):
		return "BinOpNode(%r, %r, %r)" % (self.left, self.right, self.opType)