# -*- coding: utf-8 -*-

from .BaseStmt import *
from maths.nodes import AstNode

class DisplayStmt(BaseStmt):
    content = None

    def __init__(self, content: AstNode):
        super().__init__()
        self.content = content