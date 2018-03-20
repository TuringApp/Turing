# -*- coding: utf-8 -*-
from typing import Tuple

from algo.stmts import BlockStmt
from .BaseStmt import *
from maths.nodes import AstNode

class IfStmt(BlockStmt):
    condition = AstNode

    def __init__(self, condition: AstNode, children: CodeBlock):
        super().__init__(children)
        self.condition = condition