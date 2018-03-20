# -*- coding: utf-8 -*-

from .BaseStmt import *
from maths.nodes import AstNode

class AssignStmt(BaseStmt):
    variable = None
    value = None

    def __init__(self, variable: str, value: AstNode):
        super().__init__()
        self.variable = variable
        self.value = value