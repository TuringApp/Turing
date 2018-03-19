# -*- coding: utf-8 -*-

from typing import Union

number = Union[int, float, complex]

def translate(context, string):
    return translate_backend(context, string)


def translate_backend(context, string):
    return string
