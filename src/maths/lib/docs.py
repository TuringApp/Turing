# -*- coding: utf-8 -*-

import inspect

funcs = {}
consts = {}
modules = {}


def doc(*kwargs):
    module = inspect.getmodule(inspect.stack()[1][0])
    mod_name = module.__desc__
    modules[mod_name] = module
    if mod_name not in funcs:
        funcs[mod_name] = []
    funcs[mod_name].append(kwargs)


def doc_c(*kwargs):
    module = inspect.getmodule(inspect.stack()[1][0])
    mod_name = module.__desc__
    modules[mod_name] = module
    if mod_name not in consts:
        consts[mod_name] = []
    consts[mod_name].append(kwargs)


def get_func_def(f):
    args = []
    for a in f[1]:
        if len(a) >= 4:
            args.append("%s=%s" % (a[0], a[3]))
        else:
            args.append(a[0])
    return "%s(%s)" % (f[0], ", ".join(args))
