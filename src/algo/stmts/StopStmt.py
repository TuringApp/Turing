# -*- coding: utf-8 -*-

from .BaseStmt import *


class StopStmt(BaseStmt):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[Stop]"
