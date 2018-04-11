# -*- coding: utf-8 -*-

from .BaseStmt import *


class StopStmt(BaseStmt):
    message = None

    def __init__(self, message: AstNode = None):
        super().__init__()
        self.message = message

    def __str__(self):
        return "[Stop %s]" % self.message

    def __repr__(self):
        return "StopStmt(%r)" % self.message

    def python(self) -> List[str]:
        return ["breakpoint(%s)" % ("" if self.message is None else self.message.python())]
