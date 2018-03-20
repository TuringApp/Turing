# -*- coding: utf-8 -*-


from algo.stmts import BaseStmt, CodeBlock

class BlockStmt(BaseStmt):
    children = None

    def __init__(self, children: CodeBlock):
        super().__init__()
        self.children = children
        for c in self.children:
            c.parent = self
