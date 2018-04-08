# -*- coding: utf-8 -*-
import maths.parser
from .IdentifierNode import *
from .NumberNode import *
import util.html

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
            self.is_imag_part = isinstance(left, NumberNode) and right == IdentifierNode("i")

        # check for complex
        if operator in ["+", "-"]:
            if isinstance(right, NumberNode) and isinstance(left, BinOpNode) and left.is_imag_part:
                left, right = right, left
            self.is_complex = isinstance(left, NumberNode) and isinstance(right, BinOpNode) and right.is_imag_part

        self.left = left
        self.right = right
        self.operator = operator
        self.precedence = maths.parser.Operators.get_precedence(operator)

    def __str__(self):
        return "[BinOp %s %s %s]" % (self.left, self.operator, self.right)

    def __repr__(self):
        return "BinOpNode(%r, %r, %r)" % (self.left, self.right, self.operator)

    def operand_code(self, operand: AstNode, bb=False) -> str:
        return operand.code_fix(bb) \
            if (isinstance(operand, BinOpNode) and operand.is_complex and operand.operator == self.operator) \
               or (not self.is_complex and isinstance(operand, BinOpNode) and operand.precedence < self.precedence) \
            else operand.code(bb)

    def code(self, bb=False) -> str:
        # handle complex numbers
        if self.is_imag_part:
            return "%si" % self.left.code(bb)
        op = maths.parser.Operators.pretty_print(self.operator)
        if bb:
            op = util.html.sanitize(op)
        return "%s %s %s" % (
            self.operand_code(self.left, bb), op,
            self.operand_code(self.right, bb))

    def python(self) -> str:
        op_table = {
            "^": "**",
            "XOR": "^"
        }
        op_fix = op_table.get(self.operator.upper(), self.operator.lower())
        return "((%s) %s (%s))" % (self.left.python(), op_fix, self.right.python())

    def children(self) -> List["AstNode"]:
        return [self.left, self.right]