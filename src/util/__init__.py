# -*- coding: utf-8 -*-
import os
import traceback
from typing import Union, List, Iterable

number = Union[int, float, complex]
settings = None
__version__ = None
__channel__ = None


def translate(context: str, string: str) -> str:
    return translate_backend(context, string)


def translate_backend(context: str, string: str) -> str:
    return string


def flatten(lst: Iterable) -> List:
    result = []

    for item in lst:
        if type(item) == list:
            result += flatten(item)
        else:
            result += item

    return result


def get_short_lang(lang):
    if "_" not in lang:
        return lang
    return lang[0:lang.index("_")]


def show_error():
    traceback.print_exc()
    # print(translate("MainWindow", "Error: ") + str(sys.exc_info()[1]) + "\n" + str(sys.exc_info()[2]))


def first_found_dir(dirList):
    """
    @return the first exisiting directory out of a list of available
    directories, or "." as a fallback.
    """
    for d in dirList:
        if os.path.isdir(d):
            return d
    return "."


def lstreplace(lst, a, b):
    return [b if x == a else x for x in lst]


def pairwise(lst):
    if not lst:
        return

    for i in range(len(lst) - 1):
        yield lst[i], lst[i + 1]

    yield lst[-1], None