# -*- coding: utf-8 -*-

from util.html import sanitize
from .AstNode import *


class StringNode(AstNode):
    """String node

    value -- value (str)"""
    value = None

    def __init__(self, value: str):
        super().__init__(True)
        self.value = value

    def __str__(self):
        return "[String '%s']" % self.value

    def __repr__(self):
        return "StringNode(%r)" % self.value

    def code(self, bb=False) -> str:
        if bb:
            return "[s]%s[/s]" % sanitize(self.code(False))
        return '"%s"' % repr(self.value)[1:-1]

    def python(self) -> str:
        return "(%r)" % self.value
