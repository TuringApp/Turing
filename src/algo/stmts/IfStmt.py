# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from maths.nodes import AstNode
from .BaseStmt import *


class IfStmt(BlockStmt):
    condition = AstNode

    def __init__(self, condition: AstNode, children: CodeBlock):
        super().__init__(children)
        self.condition = condition

    def __str__(self):
        return "[If %s %s]" % (self.condition, super().__str__())

    def __repr__(self):
        return "IfStmt(%r, %r)" % (self.condition, self.children)

    def python_header(self) -> str:
        return "if %s:" % self.condition.python()