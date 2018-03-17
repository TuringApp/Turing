# -*- coding: utf-8 -*-

from .AstNode import *


class BinOpNode(AstNode):
    """Binary (two operands) operator node

    left   -- left operand (AstNode)
    right  -- right operand (AstNode)
    operatir -- which binary operator (str)"""
    left = None
    right = None
    operator = None

    def __init__(self, left, right, operator):
        super().__init__()
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self):
        return "[BinOp (%s) %s (%s)]" % (self.left, self.operator, self.right)

    def __repr__(self):
        return "BinOpNode(%r, %r, %r)" % (self.left, self.right, self.operator)
