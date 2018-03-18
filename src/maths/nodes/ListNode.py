# -*- coding: utf-8 -*-

from util.math import proper_str
from .AstNode import *


class ListNode(AstNode):
    """Identifier node

    value -- value (list of object)"""
    value = None

    def __init__(self, value):
        super().__init__(True)
        self.value = value

    def __str__(self):
        return "[List %s]" % self.value

    def __repr__(self):
        return "ListNode(%r)" % self.value

    def code(self):
        return proper_str([node.code() for node in self.value])
