# -*- coding: utf-8 -*-

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