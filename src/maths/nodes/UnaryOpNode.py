# -*- coding: utf-8 -*-

from .AstNode import *


class UnaryOpNode(AstNode):
    """Unary operator node

    value  -- value (AstNode)
    operator -- which unary operator (str)"""
    value = None
    operator = None

    def __init__(self, value: AstNode, operator: str):
        super().__init__(True)
        if operator.upper() == "NON":
            operator = "NOT"
        self.value = value
        self.operator = operator

    def __str__(self):
        return "[UnaryOp %s %s]" % (self.operator, self.value)

    def __repr__(self):
        return "UnaryOpNode(%r, %r)" % (self.value, self.operator)

    def code(self, bb=False) -> str:
        return self.operator + self.value.code_fix(bb)

    def python(self) -> str:
        return "(%s (%s))" % (self.operator, self.value.python())
