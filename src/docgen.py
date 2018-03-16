# -*- coding: utf-8 -*-

import maths.lib
import itertools
import re
import os
from util.math import isint, properstr


def doc_funcs():
    ret = ""
    fns = maths.lib.get_funcs()

    for k in sorted(fns.keys()):
        ret += "|&nbsp;|**%s**|&nbsp;|\n" % k

        for f in sorted(fns[k], key=lambda x: x[0]):
            names = [f[0]]

            if len(f) > 3:
                # add alias
                names = names + f[3]

            name = " / ".join("`%s`" % x for x in names)

            # check if any parameters
            if f[1]:
                args = "<ul>"
                for arg in f[1]:
                    args += "<li>"
                    args += "`%s` (%s)" % (arg[0], arg[1])
                    if len(arg) > 2:
                        constr = arg[2]
                        if len(arg) > 3:
                            deft = "default = %s" % arg[3] if arg[3] is not None else None
                        else:
                            deft = None
                        infos = ", ".join(x for x in [constr, deft] if x)
                        if infos:
                            args += " " + infos
                    args += "</li>"
                args += "</ul>"

            # replace {{x}} by `x` for markdown
            desc = re.sub(r"{{(\w+)\}\}", "`\g<1>`", f[2])
            desc = re.sub(r"//(\w+)//", "*\g<1>*", desc)

            ret += "|%s|%s|%s|\n" % (name, args, desc)

    return ret


def doc_consts():
    ret = ""
    cts = maths.lib.get_consts()

    for k in sorted(cts.keys()):
        ret += "|&nbsp;|**%s**|&nbsp;|\n" % k

        for c in sorted(cts[k], key=lambda x: x[0]):
            name, symbol, desc = c[:3]

            actual = getattr(maths.lib.get_modules()[k], "c_" + name)

            if isint(actual):
                # if integer, only value is needed
                val = str(actual)
            else:
                if "e" in str(actual):
                    # if exponent, add pretty html
                    sig, exp = str(actual).split("e")
                    val = str(round(float(sig), 15)) + "&middot;10<sup>%d</sup>" % int(exp)
                else:
                    # otherwise, only rounded value
                    if type(actual) == complex:
                        val = properstr(actual)
                    else:
                        val = "%.15f" % actual

            unit = ""
            if len(c) > 3:
                # add unit
                unit = " (%s)" % c[3].replace("*", "&middot;")

            desc = re.sub(r"//(\w+)//", "*\g<1>*", desc)

            ret += "|`%s`|%s|*%s* - %s%s|\n" % (name, val, symbol, desc, unit)

    return ret


if __name__ == "__main__":
    path_docs = os.path.join(os.path.dirname(__file__), os.pardir, "docs")

    templ = os.path.join(path_docs, "expression_templ.md")
    outp = os.path.join(path_docs, "expression.md")

    with open(templ, "r", encoding="utf8") as f:
        templ_md = f.read()

    templ_md = templ_md.replace("{{{funcdoc}}}", doc_funcs())
    templ_md = templ_md.replace("{{{constdoc}}}", doc_consts())

    with open(outp, "w", encoding="utf8") as f:
        f.write(templ_md)
