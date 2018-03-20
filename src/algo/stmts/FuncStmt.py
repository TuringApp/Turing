# -*- coding: utf-8 -*-
from typing import List

from algo.stmts import BlockStmt
from .BaseStmt import *
from maths.nodes import AstNode


class FuncStmt(BlockStmt):
    parameters = None

    def __init__(self, parameters: List[str], children: CodeBlock):
        super().__init__(children)
        self.parameters = parameters