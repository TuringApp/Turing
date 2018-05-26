# -*- coding: utf-8 -*-
import sys, os
## add a path to get the embedded unmaintained package pyqode
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import keyword

from pyqode.core import backend

import maths.lib.docs


class PythonCompletionProvider:
    @staticmethod
    def complete(code, *args):
        return [{"name": x} for x in keyword.kwlist]


class LibCompletionProvider:
    def __init__(self):
        self.functions = [f[0] for fns in maths.lib.get_funcs().values() for f in fns]
        self.constants = [c[0] for cts in maths.lib.get_consts().values() for c in cts]
        self.directory = [{"name": x} for x in (self.functions + self.constants)]

    def complete(self, code, *args):
        return self.directory


class FinalCompletionProvider:
    def __init__(self):
        self.providers = []

    def complete(self, code, *args):
        return [c for prov in self.providers for c in prov.complete(code, args)]


if __name__ == '__main__':
    provider = FinalCompletionProvider()

    provider.providers.append(PythonCompletionProvider())
    provider.providers.append(LibCompletionProvider())

    backend.CodeCompletionWorker.providers.append(provider)
    backend.serve_forever()
