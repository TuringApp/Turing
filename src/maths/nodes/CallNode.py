# -*- coding: utf-8 -*-

from typing import List

from .AstNode import *


class CallNode(AstNode):
    """Function call node

    func -- function (AstNode)
    args -- arguments (list of AstNode)"""
    func = None
    args = None

    def __init__(self, func: AstNode, args: List[AstNode]):
        super().__init__(True)
        self.func = func
        self.args = args

    def __str__(self):
        return "[Call %s with %s]" % (self.func, self.args)

    def __repr__(self):
        return "CallNode(%r, %r)" % (self.func, self.args)

    def code(self, bb=False) -> str:
        return "%s(%s)" % (self.func.code_fix(bb), ", ".join(arg.code(bb) for arg in self.args))
