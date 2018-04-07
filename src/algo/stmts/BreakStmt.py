# -*- coding: utf-8 -*-

from .BaseStmt import *


class BreakStmt(BaseStmt):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[Break]"

    def __repr__(self):
        return "BreakStmt()"

    def python(self) -> List[str]:
        return ["break"]
