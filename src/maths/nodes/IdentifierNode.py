# -*- coding: utf-8 -*-

from .AstNode import *


class IdentifierNode(AstNode):
    """Identifier node

    value -- value (str)"""
    value = None

    def __init__(self, value: str):
        super().__init__(True)
        self.value = value

    def __str__(self):
        return "[Identifier %s]" % self.value

    def __repr__(self):
        return "IdentifierNode(%r)" % self.value

    def __eq__(self, other):
        return type(other) == IdentifierNode and other.value == self.value

    def code(self, bb=False) -> str:
        if bb:
            return "[i]%s[/i]" % self.code(False)
        return self.value

    def python(self) -> str:
        return self.value