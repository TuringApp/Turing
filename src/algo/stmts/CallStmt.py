# -*- coding: utf-8 -*-

from maths.nodes import AstNode, CallNode
from .BaseStmt import *


class CallStmt(BaseStmt):
    function = None
    arguments = None

    def __init__(self, function: AstNode, arguments: List[AstNode]):
        super().__init__()
        self.function = function
        self.arguments = arguments

    def __str__(self):
        return "[Call %s (%s)]" % (self.function, ", ".join(str(x) for x in self.arguments))

    def __repr__(self):
        return "CallStmt(%r, %r)" % (self.function, self.arguments)

    def python(self) -> List[str]:
        return ["(%s)(%s)" % (self.function.python(), ", ".join(x.python() for x in self.arguments))]

    def to_node(self):
        return CallNode(self.function, self.arguments)

    @staticmethod
    def from_node(node: CallNode):
        return CallStmt(node.func, node.args)