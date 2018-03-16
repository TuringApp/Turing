# -*- coding: utf-8 -*-

from maths.parser import *
import math
import random
from util.math import *
import maths.lib as mlib
import maths.nodes as nodes
from util.log import Logger
import sys
import types


class Evaluator:
    variables = None
    arguments = None
    log = None
    beautified = None
    strictType = False

    def round_ex(num, prec=None):
        if prec:
            return round(num, int(prec))
        return round(num)

    def __init__(self, strict=False):
        self.variables = {}

        for n, mod in mlib.__dict__.items():
            if isinstance(mod, types.ModuleType):
                for fn, func in mod.__dict__.items():
                    if callable(func):
                        self.variables[fn] = func
                    else:
                        if fn.startswith("c_"):
                            self.variables[fn[2:]] = func

        self.arguments = []
        self.log = Logger("Eval")
        self.strictType = strict

    def evaluate(self, expr):
        par = Parser(expr)
        exp = None

        if False:
            exp = par.parse()
        else:
            try:
                exp = par.parse()
            except:
                self.log.error("Parser: " + str(sys.exc_info()[1]))

        for msg in par.log.getMessages():
            self.log.messages.append(msg)

        self.beautified = par.beautify()

        if not exp:
            return None

        ret = None

        try:
            ret = self.evalNode(exp)
        except:
            raise
            self.log.error(str(sys.exc_info()[1]))

        return ret

    def evalNode(self, node):
        val = self.evalNodeReal(node)

        if val is not None and isnum(val) and not isinstance(val, bool):
            if type(val) == complex:
                if isreal(val):
                    val = val.real

            if isint(val) and 1 <= abs(val) <= 1e15:
                val = int(round(val))

            if iszero(val):
                val = 0
            else:
                val = closeround(val, 9)

        return val

    def callLambda(self, node, *args):
        args = list(args)
        if len(args) != len(node.args):
            self.log.error("Argument count mismatch (expected %d, got %d)" % (len(node.args), len(args)))
        for i in range(len(args)):
            self.arguments.append((node.args[i], args[i]))
        ret = self.evalNode(node.expr)
        for i in range(len(args)):
            self.arguments.pop()
        return ret

    def evalNodeReal(self, node):
        if type(node) == nodes.ListNode:
            return [self.evalNode(x) for x in node.value]

        if type(node) in [nodes.NumberNode, nodes.StringNode]:
            return node.value

        if type(node) == nodes.IdentifierNode:
            for a in self.arguments[::-1]:
                if a[0] == node.value:
                    return a[1]
            if node.value in self.variables:
                return self.variables[node.value]
            else:
                self.log.error("Can't find variable or function " + node.value)

        if type(node) == nodes.UnaryOpNode:
            return self.evalUnary(node)

        if type(node) == nodes.BinOpNode:
            return self.evalBinary(node)

        if type(node) == nodes.CallNode:
            fn = self.evalNode(node.func)
            if fn is None:
                return None
            args = [self.evalNode(x) for x in node.args]
            return fn.__call__(*args)

        if type(node) == nodes.ArrayAccessNode:
            val = self.evalNode(node.array)
            idx = int(self.evalNode(node.index))
            if idx < len(val):
                return val[idx]
            else:
                self.log.error("Index '%s' too big for array" % idx)

        if type(node) == nodes.LambdaNode:
            return lambda *args: self.callLambda(node, *list(args))

        if not isinstance(node, nodes.AstNode):
            return node

        return None

    def evalUnary(self, node):
        val = self.evalNode(node.value)
        vtype = ValueType.getType(val)

        if node.opType == "-" and (isnum(val) and (not self.strictType or not isbool(val))):
            return -val

        if node.opType == "-" and vtype == ValueType.LIST:
            return val[::-1]

        if node.opType == "NON" and (isbool(val) or (not self.strictType and isnum(val))):
            return not val

        self.log.error("Invalid unary operator '%s'" % node.opType)

    def evalBinary(self, node):
        left = self.evalNode(node.left)
        ltype = ValueType.getType(left)
        right = self.evalNode(node.right)
        rtype = ValueType.getType(right)

        if left is None or right is None:
            self.log.error("Trying to use None")
            return None

        if node.opType in ["*"] and rtype == ValueType.LIST and ltype != ValueType.LIST:
            (left, ltype, right, rtype) = (right, rtype, left, ltype)

        ret = None

        if self.strictType:
            if ltype != rtype:
                self.log.error("Type mismatch: operands have different type (%s and %s)" % (
                    ValueType.getName(ltype), ValueType.getName(rtype)))
                return None

            if ltype == ValueType.BOOLEAN:
                allowed = Operators.boolean
            elif ltype == ValueType.NUMBER:
                allowed = Operators.math + Operators.comp
            elif ltype == ValueType.STRING:
                allowed = Operators.eq + ["+"]
            elif ltype == ValueType.LIST:
                allowed = Operators.eq + ["+", "-", "&", "|"]
            else:
                errpos = []
                if ltype is None:
                    errpos.append("left")
                if rtype is None:
                    errpos.append("right")

                self.log.error("Invalid value type for %s and operator '%s'" % (" and ".join(errpos), node.opType))
                return None

            if node.opType not in allowed:
                self.log.error("Operator '%s' not allowed for value type %s" % (node.opType, ValueType.getName(ltype)))
                return None

        if node.opType == "+":
            ret = left + right
        elif node.opType == "-":
            if ltype == rtype == ValueType.LIST:
                ret = [x for x in left if x not in right]
            else:
                ret = left - right
        elif node.opType == "*":
            if ltype == ValueType.LIST:
                if not isint(right):
                    self.log.error("Trying to multiply List by non-integer (%f)" % right)
                    return None
                else:
                    ret = left * int(right)
            else:
                ret = left * right
        elif node.opType == "/":
            if right == 0:
                self.log.error("Trying to divide by zero")
                return None
            ret = left / right
        elif node.opType == "%":
            ret = math.fmod(left, right)
        elif node.opType == "^":
            ret = left ** right

        elif node.opType == "<=":
            ret = left <= right or isclose(left, right)
        elif node.opType == "<":
            ret = left < right
        elif node.opType == ">":
            ret = left > right
        elif node.opType == ">=":
            ret = left >= right or isclose(left, right)

        elif node.opType == "==":
            ret = isclose(left, right)
        elif node.opType == "!=":
            ret = not isclose(left, right)
        elif node.opType == "&":
            if ltype == rtype == ValueType.LIST:
                ret = [x for x in left if x in right]
            else:
                ret = int(left) & int(right)
        elif node.opType == "|":
            if ltype == rtype == ValueType.LIST:
                ret = list(set(left + right))
            else:
                ret = int(left) | int(right)
        elif node.opType == "XOR":
            if ltype == rtype == ValueType.LIST:
                ret = list(set(x for x in left + right if x not in left or x not in right))
            else:
                ret = int(left) ^ int(right)

        if ret is None:
            self.log.error("Invalid binary operator '%s' for '%s' and '%s'" % (node.opType, left, right))
        else:
            if isbool(left) and isbool(right):
                ret = bool(ret)

        return ret
