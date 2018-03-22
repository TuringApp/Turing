# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class CommentStmt(BaseStmt):
    content = None

    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def __str__(self):
        return "[Comment %s]" % self.content
