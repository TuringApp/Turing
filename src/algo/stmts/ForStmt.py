# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from algo.stmts.BlockStmt import BlockStmt
from maths.nodes import AstNode
from .BaseStmt import *


class ForStmt(BlockStmt):
    variable = None
    begin = None
    end = None
    step = None

    def __init__(self, variable: str, begin: AstNode, end: AstNode, children: CodeBlock, step: AstNode = None):
        super().__init__(children)
        self.variable = variable
        self.begin = begin
        self.end = end
        self.step = step

    def __str__(self):
        return "[For %s = %s -> %s [%s] %s]" % (self.variable, self.begin, self.end, self.step, super().__str__())

    def __repr__(self):
        return "ForStmt(%r, %r, %r, %r, %r)" % (self.variable, self.begin, self.end, self.children, self.step)

    def python_header(self) -> str:
        return "for %s in range(%s, (%s) + 1, %s):" % (self.variable, self.begin.python(), self.end.python(), 1 if self.step is None else self.step.python())