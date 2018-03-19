# -*- coding: utf-8 -*-

class AstNode:
    """Base node class"""
    atomic = False

    def __init__(self, atomic: bool = False):
        self.atomic = atomic

    def code(self) -> str:
        return "<unimplemented>"

    def code_fix(self) -> str:
        if self.atomic:
            return self.code()
        return "(%s)" % self.code()
