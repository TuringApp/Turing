# -*- coding: utf-8 -*-

class AstNode:
    """Base node class"""
    atomic = False

    def __init__(self, atomic: bool = False):
        self.atomic = atomic

    def code(self, bb=False) -> str:
        return "<unimplemented>"

    def code_fix(self, bb=False) -> str:
        if self.atomic:
            return self.code(bb)
        return "(%s)" % self.code(bb)

    def python(self) -> str:
        return "<unimplemented>"
