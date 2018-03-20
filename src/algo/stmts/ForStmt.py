# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from algo.stmts.BlockStmt import BlockStmt
from maths.nodes import AstNode, NumberNode
from .BaseStmt import *


class ForStmt(BlockStmt):
    variable = None
    begin = None
    end = None
    step = None

    def __init__(self, variable: str, begin: AstNode, end: AstNode, children: CodeBlock, step: AstNode = None):
        super().__init__(children)
        self.variable = variable
        self.begin = begin
        self.end = end
        if step == None:
            step = NumberNode(1)
        self.step = step
