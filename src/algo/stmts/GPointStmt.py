# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class GPointStmt(BaseStmt):
    x = None
    y = None
    color = None

    def __init__(self, x: AstNode, y: AstNode, color: AstNode):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return "[GPoint (%s; %s) - %s]" % (self.x, self.y, self.color)

    def __repr__(self):
        return "GPointStmt(%r, %r, %r)" % (self.x, self.y, self.color)

    def python(self) -> List[str]:
        return ["g_point(%s, %s, %s)" % (self.x.python(), self.y.python(), self.color.python())]

    def get_children(self) -> List[AstNode]:
        return self.x.flatten() + self.y.flatten() + self.color.flatten()