# -*- coding: utf-8 -*-

class AstNode:
    """Base node class"""
    atomic = False

    def __init__(self, atomic=False):
        self.atomic = atomic

    def code(self):
        return "<unimplemented>"

    def code_fix(self):
        if self.atomic:
            return self.code()
        return "(%s)" % self.code()
