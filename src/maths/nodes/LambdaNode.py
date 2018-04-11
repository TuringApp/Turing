# -*- coding: utf-8 -*-

from .AstNode import *


class LambdaNode(AstNode):
    """Lambda (inline function) node

    args -- arguments (list of str)
    expr -- expression (AstNode)"""
    args = None
    expr = None

    def __init__(self, args: List[str], expr: AstNode):
        super().__init__(True)
        self.args = args
        self.expr = expr

    def __str__(self):
        return "[Lambda %s -> %s]" % (self.args, self.expr)

    def __repr__(self):
        return "LambdaNode(%r, %r)" % (self.args, self.expr)

    def code(self, bb=False) -> str:
        return "{%s}(%s)" % (", ".join(self.args), self.expr.code(bb))

    def python(self) -> str:
        return "(lambda %s: %s)" % (", ".join(self.args), self.expr.python())

    def children(self) -> List["AstNode"]:
        return [self.expr]
