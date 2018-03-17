# -*- coding: utf-8 -*-

from .AstNode import *


class UnaryOpNode(AstNode):
    """Unary operator node

    value  -- value (AstNode)
    operator -- which unary operator (str)"""
    value = None
    operator = None

    def __init__(self, value, operator):
        super().__init__()
        self.value = value
        self.operator = operator

    def __str__(self):
        return "[UnaryOp %s (%s)]" % (self.operator, self.value)

    def __repr__(self):
        return "UnaryOpNode(%r, %r)" % (self.value, self.operator)
