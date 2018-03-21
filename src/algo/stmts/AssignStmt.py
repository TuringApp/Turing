# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class AssignStmt(BaseStmt):
    variable = None
    value = None

    def __init__(self, variable: str, value: AstNode):
        super().__init__()
        self.variable = variable
        self.value = value

    def __str__(self):
        return "[Assign %s = %s]" % (self.variable, self.value)
