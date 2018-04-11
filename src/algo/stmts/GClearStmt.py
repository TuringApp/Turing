# -*- coding: utf-8 -*-

from .BaseStmt import *


class GClearStmt(BaseStmt):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[GClear]"

    def __repr__(self):
        return "GClearStmt()"

    def python(self) -> List[str]:
        return ["g_clear()"]
