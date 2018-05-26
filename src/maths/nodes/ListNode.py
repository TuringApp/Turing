# -*- coding: utf-8 -*-

import util.html
from util.math import proper_str
from .AstNode import *


class ListNode(AstNode):
    """Identifier node

    value -- value (list of AstNode)"""

    def __init__(self, value: List[AstNode]):
        super().__init__(True)
        self.value = value

    def __str__(self):
        return "[List %s]" % self.value

    def __repr__(self):
        return "ListNode(%r)" % self.value

    def code(self, bb=False) -> str:
        return (util.html.sanitize("[%s]") if bb else "[%s]") % proper_str([node.code(bb) for node in self.value])[1:-1]

    def python(self) -> str:
        return "list([%s])" % ", ".join(x.python() for x in self.value)

    def children(self) -> List["AstNode"]:
        return self.value
