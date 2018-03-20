# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class ReturnStmt(BaseStmt):
    value = None

    def __init__(self, value: AstNode):
        super().__init__()
        self.value = value
