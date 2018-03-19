# -*- coding: utf-8 -*-
import maths.parser
from .IdentifierNode import *
from .NumberNode import *


class BinOpNode(AstNode):
    """Binary (two operands) operator node

    left   -- left operand (AstNode)
    right  -- right operand (AstNode)
    operator -- which binary operator (str)"""
    left = None
    right = None
    operator = None
    precedence = None
    is_imag_part = False
    is_complex = False

    def __init__(self, left: AstNode, right: AstNode, operator: str):
        super().__init__()

        # check for imaginary part
        if operator == "*":
            if left == IdentifierNode("i") and type(right) == NumberNode:
                left, right = right, left
            self.is_imag_part = type(left) == NumberNode and right == IdentifierNode("i")

        # check for complex
        if operator in ["+", "-"]:
            if type(right) == NumberNode and type(left) == BinOpNode and left.is_imag_part:
                left, right = right, left
            self.is_complex = type(left) == NumberNode and type(right) == BinOpNode and right.is_imag_part

        self.left = left
        self.right = right
        self.operator = operator
        self.precedence = maths.parser.Operators.get_precedence(operator)

    def __str__(self):
        return "[BinOp (%s) %s (%s)]" % (self.left, self.operator, self.right)

    def __repr__(self):
        return "BinOpNode(%r, %r, %r)" % (self.left, self.right, self.operator)

    def operand_code(self, operand: AstNode) -> str:
        return operand.code_fix() \
            if (type(operand) == BinOpNode and operand.is_complex and operand.operator == self.operator) \
               or (not self.is_complex and type(operand) == BinOpNode and operand.precedence < self.precedence) \
            else operand.code()

    def code(self) -> str:
        # handle complex numbers
        if self.is_imag_part:
            return "%si" % self.left.code()
        return "%s %s %s" % (
        self.operand_code(self.left), maths.parser.Operators.pretty_print(self.operator), self.operand_code(self.right))
