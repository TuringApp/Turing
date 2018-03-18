# -*- coding: utf-8 -*-

from util.math import proper_str
from .AstNode import *


class NumberNode(AstNode):
    """Number node

    value -- value (float)"""
    value = None

    def __init__(self, value):
        super().__init__(type(value) != complex or proper_str(value)[-1] != "i")
        self.value = value

    def __str__(self):
        return "[Number %s]" % self.value

    def __repr__(self):
        return "NumberNode(%r)" % self.value

    def code(self):
        return proper_str(self.value)
