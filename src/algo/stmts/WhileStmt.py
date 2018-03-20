# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from maths.nodes import AstNode
from .BaseStmt import *


class WhileStmt(BlockStmt):
    predicate = None

    def __init__(self, predicate: AstNode, children: CodeBlock):
        super().__init__(children)
        self.predicate = predicate
