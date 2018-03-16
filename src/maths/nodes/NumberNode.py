# -*- coding: utf-8 -*-

from .AstNode import *


class NumberNode(AstNode):
    """Number node

    value -- value (float)"""
    value = None

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return "[Number %s]" % (self.value)

    def __repr__(self):
        return "NumberNode(%r)" % (self.value)

    def code(self):
        return
