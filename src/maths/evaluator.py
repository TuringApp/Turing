# -*- coding: utf-8 -*-

import math
import sys

import maths.lib as mlib
from maths.parser import *
from util.log import Logger
from util.math import *

DEBUG = False


class Evaluator:
    frames = None
    defaults = None
    arguments = None
    log = None
    beautified = None
    strict_typing = False
    node_tree = None

    def __init__(self, strict=False):
        self.frames = []
        self.defaults = {}

        for name, item in mlib.__dict__.items():
            if isinstance(item, types.ModuleType):
                for member_name, member in item.__dict__.items():
                    if callable(member):  # if function
                        self.defaults[member_name] = member
                    elif member_name.startswith("c_"):  # if constant
                        self.defaults[member_name[2:]] = member

        self.log = Logger("Eval")
        self.strict_typing = strict

    def enter_frame(self):
        self.frames.append({})

    def exit_frame(self):
        return self.frames.pop()

    def set_variable(self, variable: str, value: object):
        for frame in reversed(self.frames):
            if variable in frame:
                frame[variable] = value
                return

        self.defaults[variable] = value

    def get_variable(self, variable: str) -> object:
        for frame in reversed(self.frames):
            if variable in frame:
                return frame[variable]

        if variable in self.defaults:
            return self.defaults[variable]

        self.log.error(translate("Evaluator", "Cannot find variable or function %s") % variable)
        return None

    def evaluate(self, expr: str) -> object:
        parser = Parser(expr)
        node = None

        try:
            node = parser.parse()
        except:
            if DEBUG:
                raise
            self.log.error(translate("Evaluator", "Parser: ") + str(sys.exc_info()[1]))

        for msg in parser.log.get_messages():
            self.log.messages.append(msg)

        self.beautified = parser.beautify()

        if not node:
            return None

        return self.evaluate_parsed(node)

    def evaluate_parsed(self, node: nodes.AstNode):
        self.node_tree = node
        self.beautified = self.node_tree.code()

        result = None

        try:
            result = self.eval_node(self.node_tree)
        except:
            if DEBUG:
                raise
            self.log.error(str(sys.exc_info()[1]))

        return result

    def eval_node(self, node: nodes.AstNode):
        """Wrapper for evalNodeReal that handles all the IEEE754 floating point rounding fuckery"""
        value = self.eval_node_real(node)

        if value is not None and is_num(value) and not isinstance(value, bool):
            if type(value) == complex:
                # if real, convert to float directly
                if is_real(value):
                    value = value.real

            # only convert to int if it fits well
            if is_int(value) and 1 <= abs(value) <= 1e15:
                value = int(round(value))

            # if zero, use zero directly
            if is_zero(value):
                value = 0
            else:
                if not (type(value) == int and value != int(float(value))):
                    value = close_round(value, 12)

        return value

    def call_lambda(self, node: nodes.LambdaNode, *args):
        """Lambda function call wrapper"""
        args = list(args)

        if len(args) != len(node.args):
            self.log.error(
                translate("Evaluator", "Argument count mismatch (expected %d, got %d)") % (len(node.args), len(args)))
            return None

        self.frames.append({node.args[idx]: arg for idx, arg in enumerate(args)})

        result = self.eval_node(node.expr)

        # pop arguments after use
        self.frames.pop()

        return result

    def eval_node_real(self, node: nodes.AstNode):
        if type(node) == nodes.ListNode:
            return [self.eval_node(x) for x in node.value]

        if type(node) in [nodes.NumberNode, nodes.StringNode]:
            return node.value

        if type(node) == nodes.IdentifierNode:
            return self.get_variable(node.value)

        if type(node) == nodes.UnaryOpNode:
            return self.eval_unary(node)

        if type(node) == nodes.BinOpNode:
            return self.eval_binary(node)

        if type(node) == nodes.CallNode:
            function = self.eval_node(node.func)

            if function is None:
                self.log.error(translate("Evaluator", "Callee is None"))
                return None

            if (len(node.args) == 1
                    and isinstance(node.args[0], nodes.UnaryOpNode)
                    and node.args[0].operator == "*"):
                # expand list of arguments
                arg_list = self.eval_node(node.args[0].value)

                if type(arg_list) != list:
                    self.log.error(translate("Evaluator", "Only lists can be expanded"))
                    return None

                args = arg_list
            else:
                args = [self.eval_node(x) for x in node.args]

            return function.__call__(*args)

        if type(node) == nodes.ArrayAccessNode:
            array = self.eval_node(node.array)
            index = int(self.eval_node(node.index))

            if index < len(array):
                return array[index]
            else:
                self.log.error(translate("Evaluator", "Index '%s' too big for array") % index)
                return None

        if type(node) == nodes.LambdaNode:
            return lambda *args: self.call_lambda(node, *list(args))

        # if the object is not a node, it must be a remnant of an already-parsed value
        # return it directly
        if not isinstance(node, nodes.AstNode):
            return node

        self.log.error(translate("Evaluator", "Unknown node type: %s") % type(node))
        return None

    def eval_unary(self, node: nodes.UnaryOpNode):
        value = self.eval_node(node.value)
        value_type = ValueType.get_type(value)

        if node.operator == "+":
            return value

        if node.operator == "-" and (is_num(value) and (not self.strict_typing or not is_bool(value))):
            return -value

        if node.operator == "-" and value_type == ValueType.LIST:
            return value[::-1]

        if node.operator == "NOT" and (is_bool(value) or (not self.strict_typing and is_num(value))):
            return not value

        self.log.error(translate("Evaluator", "Invalid unary operator '%s'") % node.operator)
        return None

    def eval_binary(self, node: nodes.BinOpNode):
        return self.binary_operation(self.eval_node(node.left), self.eval_node(node.right), node.operator)

    def binary_operation(self, left, right, operator):
        left_type = ValueType.get_type(left)
        right_type = ValueType.get_type(right)

        if left is None or right is None:
            self.log.error(translate("Evaluator", "Trying to use None"))
            return None

        if operator == "+" and ValueType.STRING in [left_type, right_type]:
            return str(left) + str(right)

        if operator in ["*"] and right_type == ValueType.LIST and left_type != ValueType.LIST:
            # if one operand is list and not the other, then put the list at left
            # so we don't have to handle both cases afterwards
            (left, left_type, right, right_type) = (right, right_type, left, left_type)

        result = None

        if self.strict_typing:
            if left_type != right_type:
                self.log.error(translate("Evaluator", "Type mismatch: operands have different types (%s and %s)") % (
                    ValueType.get_name(left_type), ValueType.get_name(right_type)))
                return None

            if left_type == ValueType.BOOLEAN:
                allowed = Operators.boolean
            elif left_type == ValueType.NUMBER:
                allowed = Operators.math + Operators.comp
            elif left_type == ValueType.STRING:
                allowed = Operators.eq + ["+"]
            elif left_type == ValueType.LIST:
                allowed = Operators.eq + ["+", "-", "&", "|"]
            else:
                error_pos = []

                if left_type is None:
                    error_pos.append(translate("Evaluator", "left"))

                if right_type is None:
                    error_pos.append(translate("Evaluator", "right"))

                self.log.error(translate("Evaluator", "Invalid value type for %s and operator '%s'") % (
                    translate("Evaluator", " and ").join(error_pos), operator))
                return None

            if operator not in allowed:
                self.log.error(
                    translate("Evaluator", "Operator '%s' not allowed for value type %s") % (
                        operator, ValueType.get_name(left_type)))
                return None

        # arithmetic
        if operator == "+":
            result = left + right
        elif operator == "-":
            if left_type == right_type == ValueType.LIST:
                result = [x for x in left if x not in right]
            else:
                result = left - right
        elif operator == "*":
            if left_type == ValueType.LIST:
                if not is_int(right):
                    self.log.error(translate("Evaluator", "Trying to multiply List by non-integer (%s)") % right)
                    return None
                else:
                    result = left * int(right)
            else:
                result = left * right
        elif operator == "/":
            if right == 0:
                self.log.error(translate("Evaluator", "Trying to divide by zero"))
                return None
            result = left / right
        elif operator == "%":
            result = math.fmod(left, right)
        elif operator in ["^", "**"]:
            result = left ** right

        # comparison
        elif operator == "<=":
            result = left <= right or is_close(left, right)
        elif operator == "<":
            result = left < right
        elif operator == ">":
            result = left > right
        elif operator == ">=":
            result = left >= right or is_close(left, right)

        # equality
        elif operator == "==":
            result = is_close(left, right)
        elif operator == "!=":
            result = not is_close(left, right)

        # logic / bitwise
        elif operator == "&":
            if left_type == right_type == ValueType.LIST:
                result = [x for x in left if x in right]
            else:
                result = int(left) & int(right)
        elif operator == "|":
            if left_type == right_type == ValueType.LIST:
                result = list(set(left + right))
            else:
                result = int(left) | int(right)
        elif operator == "XOR":
            if left_type == right_type == ValueType.LIST:
                result = list(set(x for x in left + right if x not in left or x not in right))
            else:
                result = int(left) ^ int(right)

        if result is None:
            self.log.error(
                translate("Evaluator", "Invalid binary operator '%s' for '%s' and '%s'") % (operator, left, right))
        else:
            if is_bool(left) and is_bool(right):
                # if both operands are bool, then cast the whole thing to bool so it looks like we're professional
                result = bool(result)

        return result
