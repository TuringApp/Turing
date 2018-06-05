# -*- coding: utf-8 -*-
from typing import List
from shlex import shlex # lexer module for shell-mode expressions

class AstNode:
    """Base node class"""

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

    def children(self) -> List["AstNode"]:
        return []

    def flatten(self) -> List["AstNode"]:
        return [self] + self.children()

def isSimple(s):
    """
    @ param s a string which may be a left or a right operand
    @return True when s is a "simple" string. A sting is "simple"
    when it is enclosed in parentheses or when it contains a single
    toke, according to shlex
    """
    return len(list(shlex(s)))==1 or \
        (s[0]=='(' and s[-1]==')')

def protectExpr(s):
    """
    protects a string by surrounding parentheses when it is not simple
    @param s a string which may be a left or a right operand
    """
    if isSimple(s):
        return s
    return '('+s+')'

