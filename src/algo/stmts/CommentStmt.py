# -*- coding: utf-8 -*-

from .BaseStmt import *


class CommentStmt(BaseStmt):
    content = None

    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def __str__(self):
        return "[Comment %s]" % self.content

    def __repr__(self):
        return "CommentStmt(%r)" % self.content

    def python(self) -> List[str]:
        return ["# " + self.content]