# -*- coding: utf-8 -*-

from .BaseStmt import *


class SleepStmt(BaseStmt):
    def __init__(self, value: AstNode):
        super().__init__()
        self.duration = value

    def __str__(self):
        return "[Sleep %s]" % self.duration

    def __repr__(self):
        return "SleepStmt(%r)" % self.duration

    def python(self) -> List[str]:
        return ["sleep (%s)" % self.duration.python()]

    def get_children(self) -> List[AstNode]:
        return self.duration.flatten()
