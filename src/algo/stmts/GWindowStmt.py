# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class GWindowStmt(BaseStmt):
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    x_grad = None
    y_grad = None

    def __init__(self, x_min: AstNode, x_max: AstNode, y_min: AstNode, y_max: AstNode, x_grad: AstNode, y_grad: AstNode):
        super().__init__()
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_grad = x_grad
        self.y_grad = y_grad

    def __str__(self):
        return "[Window X(%s; %s) Y(%s; %s) Grad(%s; %s)]" % (self.x_min, self.x_max, self.y_min, self.y_max, self.x_grad, self.y_grad)

    def __repr__(self):
        return "GWindowStmt(%r, %r, %r, %r, %r, %r)" % (self.x_min, self.x_max, self.y_min, self.y_max, self.x_grad, self.y_grad)

    def python(self) -> List[str]:
        return ["g_window(%s, %s, %s, %s, %s, %s)" % (self.x_min.python(), self.x_max.python(), self.y_min.python(), self.y_max.python(), self.x_grad.python(), self.y_grad.python())]

    def get_children(self) -> List[AstNode]:
        return [x for c in (self.x_min, self.x_max, self.y_min, self.y_max, self.x_grad, self.y_grad) for x in c.flatten()]