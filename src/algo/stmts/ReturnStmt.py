# -*- coding: utf-8 -*-

from .BaseStmt import *


class ReturnStmt(BaseStmt):
    def __init__(self, value: AstNode = None):
        super().__init__()
        self.value = value

    def __str__(self):
        return "[Return %s]" % self.value

    def __repr__(self):
        return "ReturnStmt(%r)" % self.value

    def python(self) -> List[str]:
        if self.value is None:
            return ["return"]
        return ["return (%s)" % self.value.python()]

    def get_children(self) -> List[AstNode]:
        return [] if self.value is None else self.value.flatten()
