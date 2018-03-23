# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from .BaseStmt import *


class FuncStmt(BlockStmt):
    name = None
    parameters = None

    def __init__(self, name: str, parameters: List[str], children: CodeBlock):
        super().__init__(children)
        self.name = name
        self.parameters = parameters

    def __str__(self):
        return "[Func %s (%s) %s]" % (self.name, ", ".join(self.parameters), super().__str__())

    def __repr__(self):
        return "FuncStmt(%r, %r, %r)" % (self.name, self.parameters, self.children)
