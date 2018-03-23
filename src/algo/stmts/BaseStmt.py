# -*- coding: utf-8 -*-

from typing import List


class BaseStmt:
    parent = None

    def __init__(self):
        pass

    def __repr__(self):
        return "BaseStmt()"


CodeBlock = List[BaseStmt]
