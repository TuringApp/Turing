# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from .BaseStmt import *


class WhileStmt(BlockStmt):
    condition = None

    def __init__(self, condition: AstNode, children: CodeBlock):
        super().__init__(children)
        self.condition = condition

    def __str__(self):
        return "[While %s %s]" % (self.condition, super().__str__())

    def __repr__(self):
        return "WhileStmt(%r, %r)" % (self.condition, self.children)

    def python_header(self) -> str:
        return "while %s:" % self.condition.python()

    def get_children(self) -> List[AstNode]:
        return self.condition.flatten() + super().get_children()
