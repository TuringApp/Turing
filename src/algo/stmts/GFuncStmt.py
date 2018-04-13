# -*- coding: utf-8 -*-
from maths.nodes import LambdaNode
from .BaseStmt import *


class GFuncStmt(BaseStmt):
    var = None
    expr = None
    start = None
    end = None
    step = None
    color = None

    def __init__(self, var: str, expr: AstNode, start: AstNode, end: AstNode, step: AstNode, color: AstNode):
        super().__init__()
        self.var = var
        self.expr = expr
        self.start = start
        self.end = end
        self.step = step
        self.color = color

    def __str__(self):
        return "[Func (%s) -> (%s) [%s; %s] / %s - %s]" % (self.var, self.expr, self.start, self.end, self.step, self.color)

    def __repr__(self):
        return "GFuncStmt(%r, %r, %r, %r, %r, %r)" % (self.var, self.expr, self.start, self.end, self.step, self.color)

    def get_function(self) -> LambdaNode:
        return LambdaNode([self.var], self.expr)

    def python(self) -> List[str]:
        return ["g_func(%s)" % ", ".join(x.python() for x in (self.get_function(), self.start, self.end, self.step, self.color))]

    def get_children(self) -> List[AstNode]:
        return [x for c in (self.expr, self.start, self.end, self.step, self.color) for x in c.flatten()]
