# -*- coding: utf-8 -*-

from .AstNode import *

class IdentifierNode(AstNode):
	"""Identifier node

	value -- value (str)"""
	value = None

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "[Identifier %s]" % self.value

	def __repr__(self):
		return "IdentifierNode(%r)" % self.value