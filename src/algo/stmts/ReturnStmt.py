# -*- coding: utf-8 -*-
from typing import List

from .BaseStmt import *
from maths.nodes import AstNode


class ReturnStmt(BaseStmt):
    value = None

    def __init__(self, value: AstNode):
        super().__init__()
        self.value = value