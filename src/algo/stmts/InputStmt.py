# -*- coding: utf-8 -*-

from maths.nodes import AstNode
from .BaseStmt import *
from util import translate

class InputStmt(BaseStmt):
    variable = None
    prompt = None

    def __init__(self, variable: AstNode, prompt: AstNode = None):
        super().__init__()
        self.variable = variable
        self.prompt = prompt

    def __str__(self):
        return "[Input '%s' -> %s]" % (self.prompt, self.variable)

    def __repr__(self):
        return "InputStmt(%r, %r)" % (self.variable, self.prompt)

    def python(self) -> List[str]:
        return ["%s = input(%s)" % (self.variable.python(), ('"%s"' % translate("Algo", "Variable {var} = ").format(var=self.variable.python())) if self.prompt is None else self.prompt.python())]

    def get_children(self) -> List[AstNode]:
        return self.variable.flatten() + ([] if self.prompt is None else self.prompt.flatten())