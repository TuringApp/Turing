# -*- coding: utf-8 -*-

from util.math import proper_str
from .AstNode import *
from typing import List

class ListNode(AstNode):
    """Identifier node

    value -- value (list of AstNode)"""
    value = None

    def __init__(self, value: List[AstNode]):
        super().__init__(True)
        self.value = value

    def __str__(self):
        return "[List %s]" % self.value

    def __repr__(self):
        return "ListNode(%r)" % self.value

    def code(self) -> str:
        return proper_str([node.code() for node in self.value])
