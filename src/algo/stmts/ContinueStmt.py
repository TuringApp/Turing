# -*- coding: utf-8 -*-

from .BaseStmt import *


class ContinueStmt(BaseStmt):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[Continue]"

    def __repr__(self):
        return "ContinueStmt()"

    def python(self) -> List[str]:
        return ["continue"]
