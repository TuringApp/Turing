# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class InputStmt(BaseStmt):
    variable = None
    prompt = None

    def __init__(self, variable: str, prompt: AstNode = None):
        super().__init__()
        self.variable = variable
        self.prompt = prompt

    def __str__(self):
        return "[Input '%s' -> %s]" % (self.prompt, self.variable)