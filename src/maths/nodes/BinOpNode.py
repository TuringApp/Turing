# -*- coding: utf-8 -*-
import maths.parser
import util.html
from .AstNode import *
from .IdentifierNode import *
from .NumberNode import *
from .StringNode import StringNode


class BinOpNode(AstNode):
    """Binary (two operands) operator node

    left   -- left operand (AstNode)
    right  -- right operand (AstNode)
    operator -- which binary operator (str)"""

    def __init__(self, left: AstNode, right: AstNode, operator: str):
        super().__init__()

        # check for imaginary part
        if operator == "*":
            if left == IdentifierNode("i") and type(right) == NumberNode:
                left, right = right, left
            self.is_imag_part = isinstance(left, NumberNode) and right == IdentifierNode("i")
        else:
            self.is_imag_part = False

        # check for complex
        if operator in ["+", "-"]:
            if isinstance(right, NumberNode) and isinstance(left, BinOpNode) and left.is_imag_part:
                left, right = right, left
            self.is_complex = isinstance(left, NumberNode) and isinstance(right, BinOpNode) and right.is_imag_part
        else:
            self.is_complex = False

        self.left = left
        self.right = right
        self.operator = operator
        self.precedence = maths.parser.Operators.get_precedence(operator)

    def __str__(self):
        return "[BinOp %s %s %s]" % (self.left, self.operator, self.right)

    def __repr__(self):
        return "BinOpNode(%r, %r, %r)" % (self.left, self.right, self.operator)

    def need_fix(self, operand: AstNode, right=False) -> bool:
        return (isinstance(operand, BinOpNode) and operand.is_complex and operand.operator == self.operator) \
               or (not self.is_complex and isinstance(operand, BinOpNode) and (operand.precedence < self.precedence or (
                right and operand.precedence == self.precedence and not maths.parser.Operators.is_commutative(
            self.operator))))

    def operand_code(self, operand: AstNode, bb=False, right=False) -> str:
        return operand.code_fix(bb) \
            if self.need_fix(operand, right) \
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
            self.operand_code(self.right, bb, True))

    def python(self) -> str:

        op_table = {
            "^": "**",
            "XOR": "^"
        }
        op_fix = op_table.get(self.operator.upper(), self.operator.lower())
        left = self.left
        right = self.right

        left_py = left.python()
        right_py = right.python()

        if op_fix == "+":
            if type(left) == StringNode and type(right) != StringNode:
                right_py = "str(%s)" % right_py

            elif type(right) == StringNode and type(left) != StringNode:
                left_py = "str(%s)" % left_py

        return "%s %s %s" % \
               (protectExpr(left_py), op_fix, protectExpr(right_py))

    def children(self) -> List["AstNode"]:
        return [self.left, self.right]
