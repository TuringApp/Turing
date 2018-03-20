# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class DisplayStmt(BaseStmt):
    content = None

    def __init__(self, content: AstNode):
        super().__init__()
        self.content = content

    def __str__(self):
        return "[Display %s]" % self.content