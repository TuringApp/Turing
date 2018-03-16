# -*- coding: utf-8 -*-

from .AstNode import *


class ArrayAccessNode(AstNode):
    """Array access node

    array -- array (AstNode)
    index -- index (AstNode)"""
    array = None
    index = None

    def __init__(self, array, index):
        super().__init__()
        self.array = array
        self.index = index

    def __str__(self):
        return "[ArrayAccess (%s) @ (%s)]" % (self.array, self.index)

    def __repr__(self):
        return "ArrayAccessNode(%r, %r)" % (self.array, self.index)
