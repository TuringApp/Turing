# -*- coding: utf-8 -*-

from .BaseStmt import *


class GLineStmt(BaseStmt):
    start_x = None
    start_y = None
    end_x = None
    end_y = None
    color = None

    def __init__(self, start_x: AstNode, start_y: AstNode, end_x: AstNode, end_y: AstNode, color: AstNode):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color

    def __str__(self):
        return "[Line (%s; %s) -> (%s; %s) - %s]" % (self.start_x, self.start_y, self.end_x, self.end_y, self.color)

    def __repr__(self):
        return "GLineStmt(%r, %r, %r, %r, %r)" % (self.start_x, self.start_y, self.end_x, self.end_y, self.color)

    def python(self) -> List[str]:
        return ["g_line(%s, %s, %s, %s, %s)" % (
        self.start_x.python(), self.start_y.python(), self.end_x.python(), self.end_y.python(), self.color.python())]

    def get_children(self) -> List[AstNode]:
        return [x for c in (self.start_x, self.start_y, self.end_x, self.end_y, self.color) for x in c.flatten()]
