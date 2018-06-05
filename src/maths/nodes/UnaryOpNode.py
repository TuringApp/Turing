# -*- coding: utf-8 -*-

import util.html
from .AstNode import *


class UnaryOpNode(AstNode):
    """Unary operator node

    value  -- value (AstNode)
    operator -- which unary operator (str)"""

    def __init__(self, value: AstNode, operator: str):
        super().__init__(True)
        if operator.upper() == "NON":
            operator = "NOT"
        self.value = value
        self.operator = operator.upper()

    def __str__(self):
        return "[UnaryOp %s %s]" % (self.operator, self.value)

    def __repr__(self):
        return "UnaryOpNode(%r, %r)" % (self.value, self.operator)

    def code(self, bb=False) -> str:
        op = self.operator
        if bb:
            op = util.html.sanitize(op)
        if op == "NOT":
            op += " "
        return op + self.value.code_fix(bb)

    def python(self) -> str:
        return "(%s %s)" % (self.operator.lower(), protectExpr(self.value.python()))

    def children(self) -> List["AstNode"]:
        return [self.value]
