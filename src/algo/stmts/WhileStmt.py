# -*- coding: utf-8 -*-
from typing import List

from algo.stmts import BlockStmt
from .BaseStmt import *
from maths.nodes import AstNode


class WhileStmt(BlockStmt):
    predicate = None

    def __init__(self, predicate: AstNode, children: CodeBlock):
        super().__init__(children)
        self.predicate = predicate