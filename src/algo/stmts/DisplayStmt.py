# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class DisplayStmt(BaseStmt):
    content = None
    newline = None

    def __init__(self, content: AstNode, newline: bool = True):
        super().__init__()
        self.content = content
        self.newline = newline

    def __str__(self):
        return "[Display %s]" % self.content

    def __repr__(self):
        return "DisplayStmt(%r)" % self.content

    def python(self) -> List[str]:
        return [("print(%s)" if self.newline else "print(%s, end='')") % self.content.code()]

    def get_children(self) -> List[AstNode]:
        return self.content.flatten()