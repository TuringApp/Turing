# -*- coding: utf-8 -*-

from util import translate
from .BaseStmt import *


class InputStmt(BaseStmt):
    variable = None
    prompt = None

    def __init__(self, variable: AstNode, prompt: AstNode = None, text: bool = False):
        super().__init__()
        self.variable = variable
        self.prompt = prompt
        self.text = text

    def __str__(self):
        return "[Input '%s' [%s] -> %s]" % (self.prompt, self.text, self.variable)

    def __repr__(self):
        return "InputStmt(%r, %r, %r)" % (self.variable, self.prompt, self.text)

    def python(self) -> List[str]:
        return ["%s = input(%s%s)" % (self.variable.python(), ('"%s"' % translate("Algo", "Variable {var} = ").format(
            var=self.variable.python())) if self.prompt is None else self.prompt.python(),
                                      "unsafe=True" if not self.text else "")]

    def get_children(self) -> List[AstNode]:
        return self.variable.flatten() + ([] if self.prompt is None else self.prompt.flatten())
