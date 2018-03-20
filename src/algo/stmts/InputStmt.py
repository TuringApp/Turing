# -*- coding: utf-8 -*-

from .BaseStmt import *
from util import translate
from maths.nodes import AstNode

class InputStmt(BaseStmt):
    variable = None
    prompt = None

    def __init__(self, variable: str, prompt: AstNode = None):
        super().__init__()
        self.variable = variable
        self.prompt = prompt