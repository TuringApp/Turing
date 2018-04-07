# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from .BaseStmt import *


class ElseStmt(BlockStmt):
    def __init__(self, children: CodeBlock):
        super().__init__(children)

    def __str__(self):
        return "[Else %s]" % (super().__str__())

    def __repr__(self):
        return "ElseStmt(%r)" % self.children

    def python_header(self) -> str:
        return "else:"
