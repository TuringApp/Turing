# -*- coding: utf-8 -*-


from algo.stmts import BaseStmt, CodeBlock


class BlockStmt(BaseStmt):
    children = None

    def __init__(self, children: CodeBlock):
        super().__init__()
        self.set_children(children)

    def __str__(self):
        return "{ %s }" % ", ".join(str(x) for x in self.children)

    def set_children(self, children: CodeBlock):
        self.children = children
        for c in self.children:
            c.parent = self