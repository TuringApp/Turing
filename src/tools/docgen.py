# -*- coding: utf-8 -*-

import os
import re

import maths.lib
from util.math import is_int, proper_str


def doc_funcs():
    result = ""
    functions = maths.lib.get_funcs()

    for category in sorted(functions.keys()):
        result += "|&nbsp;|**%s**|&nbsp;|\n" % category

        for function in sorted(functions[category], key=lambda x: x[0]):
            names = [function[0]]

            if len(function) > 3:
                # add alias
                names = names + function[3]

            name = " / ".join("`%s`" % x for x in names)

            # check if any parameters
            args = "<ul>"
            if function[1]:
                for arg in function[1]:
                    args += "<li>"

                    args += "`%s` (%s)" % (arg[0], arg[1])
                    if len(arg) > 2:
                        constraint = arg[2]

                        if len(arg) > 3:
                            default = "default = %s" % arg[3] if arg[3] is not None else None
                        else:
                            default = None

                        arg_infos = ", ".join(x for x in [constraint, default] if x)

                        if arg_infos:
                            args += " " + arg_infos

                    args += "</li>"
            else:
                args += "<li>None</li>"

            args += "</ul>"

            # replace {{x}} by `x` for markdown
            desc = re.sub(r"{{(\w+)\}\}", "`\g<1>`", function[2])
            desc = re.sub(r"//(\w+)//", "*\g<1>*", desc)

            result += "|%s|%s|%s|\n" % (name, args, desc)

    return result


def doc_consts():
    result = ""
    constants = maths.lib.get_consts()

    for category in sorted(constants.keys()):
        result += "|&nbsp;|**%s**|&nbsp;|\n" % category

        for constant in sorted(constants[category], key=lambda x: x[0]):
            name, symbol, desc = constant[:3]

            actual = getattr(maths.lib.get_modules()[category], "c_" + name)

            if is_int(actual):
                # if integer, only value is needed
                value = str(actual)
            else:
                if "e" in str(actual):
                    # if exponent, add pretty html
                    sig, exp = str(actual).split("e")
                    value = str(round(float(sig), 15)) + "&middot;10<sup>%d</sup>" % int(exp)
                else:
                    # otherwise, only rounded value
                    if type(actual) == complex:
                        value = proper_str(actual)
                    else:
                        value = "%.15f" % actual

            unit = ""

            if len(constant) > 3:
                # add unit
                unit = " (%s)" % constant[3].replace("*", "&middot;")

            desc = re.sub(r"//(\w+)//", "*\g<1>*", desc)

            result += "|`%s`|%s|*%s* - %s%s|\n" % (name, value, symbol, desc, unit)

    return result


if __name__ == "__main__":
    path_docs = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "docs")

    template = os.path.join(path_docs, "expression_templ.md")
    output = os.path.join(path_docs, "expression.md")

    with open(template, "r", encoding="utf8") as file:
        markdown = file.read()

    markdown = markdown.replace("{{{funcdoc}}}", doc_funcs())
    markdown = markdown.replace("{{{constdoc}}}", doc_consts())

    with open(output, "w", encoding="utf8") as file:
        file.write(markdown)
