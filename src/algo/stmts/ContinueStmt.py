# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *


class ContinueStmt(BaseStmt):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[Continue]"