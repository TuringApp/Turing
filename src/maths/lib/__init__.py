# -*- coding: utf-8 -*-
from typing import Optional, Tuple

import maths.lib.basic
import maths.lib.cast
import maths.lib.const
import maths.lib.docs
import maths.lib.geom
import maths.lib.physics
import maths.lib.stats
import maths.lib.trig


def get_funcs():
    return docs.funcs


def get_consts():
    return docs.consts


def get_modules():
    return docs.modules


def find_function(name: str) -> Optional[Tuple[str, Tuple]]:
    functions = get_funcs()
    for k in functions:
        for f in functions[k]:
            if f[0] == name:
                return k, f

    return None
