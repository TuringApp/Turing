# -*- coding: utf-8 -*-

from algo.stmts import BlockStmt
from .BaseStmt import *


class ElseStmt(BlockStmt):
    def __init__(self, children: CodeBlock):
        super().__init__(children)

    def __str__(self):
        return "[Else %s]" % (super().__str__())
