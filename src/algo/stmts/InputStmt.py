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
