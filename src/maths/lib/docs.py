# -*- coding: utf-8 -*-

import inspect
import sys

from util.math import proper_str

funcs = {}
consts = {}
modules = {}
ext_aliases = {}


def doc(*kwargs):
    module = sys.modules[inspect.stack()[1][0].f_globals["__name__"]]
    mod_name = module.__desc__
    modules[mod_name] = module
    if mod_name not in funcs:
        funcs[mod_name] = []
    funcs[mod_name].append(kwargs)


def doc_c(*kwargs):
    module = sys.modules[inspect.stack()[1][0].f_globals["__name__"]]
    mod_name = module.__desc__
    modules[mod_name] = module
    if mod_name not in consts:
        consts[mod_name] = []
    consts[mod_name].append(kwargs)


def add_alias(func, alias):
    ext_aliases[alias] = func


def get_func_def(f):
    args = []
    for a in f[1]:
        if len(a) >= 4:
            args.append("%s=%s" % (a[0], proper_str(a[3])))
        else:
            args.append(a[0])
    return "%s(%s)" % (f[0], ", ".join(args))


def get_func_def_html(f, name_bold=True):
    hargs = []
    name = f[0]
    if name_bold:
        name = "<b>%s</b>" % name
    for a in f[1]:
        cur = "<i><b>%s</b></i>" % a[0]
        if len(a) >= 4:
            cur += "=%s" % proper_str(a[3])
        hargs.append(cur)

    return "%s(%s)" % (name, ", ".join(hargs))
