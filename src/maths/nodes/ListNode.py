# -*- coding: utf-8 -*-

from .AstNode import *

class ListNode(AstNode):
	"""Identifier node

	value -- value (list of object)"""
	value = None

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "[List %s]" % (self.value)

	def __repr__(self):
		return "ListNode(%r)" % (self.value)