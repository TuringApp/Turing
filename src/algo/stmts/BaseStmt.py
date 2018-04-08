# -*- coding: utf-8 -*-

from typing import List

from maths.nodes import AstNode


class BaseStmt:
    parent = None

    def __init__(self):
        pass

    def __repr__(self):
        return "BaseStmt()"

    def python(self) -> List[str]:
        return [""]

    def get_children(self) -> List[AstNode]:
        return []


CodeBlock = List[BaseStmt]
