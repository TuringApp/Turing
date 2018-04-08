# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class AssignStmt(BaseStmt):
    variable = None
    value = None

    def __init__(self, variable: AstNode, value: AstNode = None):
        super().__init__()
        self.variable = variable
        self.value = value

    def __str__(self):
        return "[Assign %s = %s]" % (self.variable, self.value)

    def __repr__(self):
        return "AssignStmt(%r, %r)" % (self.variable, self.value)

    def python(self) -> List[str]:
        return ["%s = %s" % (self.variable.python(), self.value.python())]

    def get_children(self) -> List[AstNode]:
        return self.variable.flatten() + self.value.flatten()