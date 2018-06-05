# -*- coding: utf-8 -*-

import util
from util.math import proper_str
from .AstNode import *


class NumberNode(AstNode):
    """Number node

    value -- value (number)"""

    def __init__(self, value: util.number):
        super().__init__(type(value) != complex or proper_str(value)[-1] != "i")
        self.value = value

    def __str__(self):
        return "[Number %s]" % self.value

    def __repr__(self):
        return "NumberNode(%r)" % self.value

    def code(self, bb=False) -> str:
        if bb:
            return "[n]%s[/n]" % self.code(False)
        return proper_str(self.value)

    def python(self) -> str:
        if type(self.value) == complex or self.value < 0:
            # parentheses for complex and negative numbers
            return "(%r)" % self.value
        # no parentheses by default
        return "%r" % self.value
