# -*- coding: utf-8 -*-

from util.math import proper_str
from .AstNode import *
import util

class NumberNode(AstNode):
    """Number node

    value -- value (number)"""
    value = None

    def __init__(self, value: util.number):
        super().__init__(type(value) != complex or proper_str(value)[-1] != "i")
        self.value = value

    def __str__(self):
        return "[Number %s]" % self.value

    def __repr__(self):
        return "NumberNode(%r)" % self.value

    def code(self) -> str:
        return proper_str(self.value)
