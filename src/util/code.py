# -*- coding: utf-8 -*-

def python_wrapper(input: str) -> str:
    return """# -*- coding: utf-8 -*-
import maths.lib
import types
for n, x in maths.lib.__dict__.items():
    if type(x) == types.ModuleType and "maths.lib." in x.__name__:
        module = __import__(x.__name__, globals(), locals(), ["*"], 0)
        for k, i in module.__dict__.items():
            if type(i) == types.FunctionType:
                globals()[k] = getattr(module, k)
del maths, types, n, x
#PersonalSavedCode :

%s
""" % input
