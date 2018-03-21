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
