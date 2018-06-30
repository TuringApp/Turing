# -*- coding: utf-8 -*-

import util.html
from .AstNode import *


class ArrayAccessNode(AstNode):
    """Array access node

    array -- array (AstNode)
    index -- index (AstNode)"""

    def __init__(self, array: AstNode, index: AstNode):
        super().__init__(True)
        self.array = array
        self.index = index

    def __str__(self):
        return "[ArrayAccess %s @ %s]" % (self.array, self.index)

    def __repr__(self):
        return "ArrayAccessNode(%r, %r)" % (self.array, self.index)

    def code(self, bb=False) -> str:
        return (util.html.escape_brackets("%s[%s]") if bb else "%s[%s]") % (
            self.array.code_fix(bb), self.index.code(bb))

    def python(self) -> str:
        return "%s[%s]" % (protectExpr(self.array.python()), self.index.python())

    def children(self) -> List["AstNode"]:
        return [self.array, self.index]
