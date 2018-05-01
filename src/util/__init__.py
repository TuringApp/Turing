# -*- coding: utf-8 -*-
import traceback
from typing import Union, List, Iterable

number = Union[int, float, complex]


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