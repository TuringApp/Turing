# -*- coding: utf-8 -*-

from typing import List


class BaseStmt():
    parent = None

    def __init__(self):
        pass


CodeBlock = List[BaseStmt]
