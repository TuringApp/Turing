# -*- coding: utf-8 -*-

import numbers
from typing import Union, Any

import util
from util import translate


def is_close(a: Union[util.number, list], b: Union[util.number, list], rel_tol=1e-8, abs_tol=1e-8) -> bool:
    """Checks if the specified numbers are close enough to be considered equal.

    Due to the usage of IEEE754 floating points number in Python, formulae like 0.1+0.2
    can lead to surprising results different from 0.3, for example 0.2999999999 and similar oddities.
    This function only compares the numbers up to a certain precision (by default 10^-9).

    a       -- first number
    b       -- second number
    rel_tol -- relative tolerance (number of digits)
    abs_tol -- absolute tolerance

    Note: this function was added in Python 3.5, thus this implementation is added to allow Turing to run on older
    versions."""

    # if only one of the two is Infinity, then they are not identical
    if type(a) == type(b) == list:
        return all(is_close(x, y) for x, y in zip(a, b))

    if type(a) == complex or type(b) == complex:
        a = complex(a)
        b = complex(b)

    if type(a) == complex and type(b) == complex:
        return is_close(a.real, b.real) and is_close(a.imag, b.imag)

    if a == float("inf") and b != float("inf") or a != float("inf") and b == float("inf"):
        return False

    # if Python already considers the numbers to be identical, no need to waste CPU cycles for that
    if a == b:
        return True

    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def is_num(a: Any) -> bool:
    """Checks if the specified Python object is a number (int, float, long, etc)."""
    return isinstance(a, numbers.Number)


def is_bool(a: Any) -> bool:
    """Checks if the specified Python object is a boolean."""
    return type(a) == bool


def is_real(a: util.number) -> bool:
    """Checks if the specified complex number is real (imaginary part is zero)."""
    if not is_num(a):
        return False

    if type(a) != complex:
        return True

    return is_zero(a.imag)


def is_int(a: util.number) -> bool:
    """Checks if the specified float is integral."""
    if type(a) == int:
        return True

    if type(a) == complex:
        return is_real(a) and is_int(a.real)

    if not is_num(a) or abs(a) == float("inf"):
        return False

    return a == 0 or (1 <= abs(a) <= 1e15 and is_close(a, round(a)))


def is_zero(a: util.number) -> bool:
    """Checks if the specified number is close enough to zero to be considered equal to zero."""
    if a == 0:
        return True

    if type(a) == complex:
        return is_zero(a.real) and is_zero(a.imag)

    if type(a) != float:
        return False

    if "e" in str(a):
        sig, exp = str(a).split("e")
        if is_int(float(sig)):
            return False

    return is_close(a, 0)


def is_proper_num(a: util.number) -> bool:
    """Checks if the specified number is a real number (excluding booleans)."""
    return is_num(a) and not is_bool(a)


def expon_round(a: float, prec: int = None) -> float:
    """Rounds the left part of a two-part float."""
    if type(a) != float:
        return a

    if "e" not in str(a):
        return round(a, prec)

    sig, exp = str(a).split("e")

    return float("%se%s" % (round(float(sig), prec), exp))


def close_round(a: util.number, prec: int = None) -> util.number:
    """If the number is close enough to its rounded version, returns the rounded version, otherwise returns the
    original number """
    if a is None:
        return 0

    if type(a) == complex:
        # rounding a complex number -> round both parts
        return complex(close_round(a.real, prec), close_round(a.imag, prec))

    if type(a) == int:
        return a

    if type(a) != float:
        return a

    if "e" in str(a):
        sig, exp = str(a).split("e")
        sig = float(sig)

        rnd = round(sig, prec)

        if is_close(rnd, sig):
            sig = rnd

        return float(str(sig) + "e" + exp)
    else:
        rnd = round(a, prec)

        if is_close(rnd, a):
            return rnd

    return a


def proper_str(a: Any) -> str:
    """Converts the specified float to string, removing comma if the number is integral."""
    if type(a) == list:
        return "[%s]" % ", ".join(proper_str(x) for x in a)

    if not is_num(a):
        return str(a)

    if is_bool(a):
        return translate("Utilities", "TRUE") if a else translate("Utilities", "FALSE")

    if type(a) == complex:
        real = None if is_zero(a.real) else proper_str(a.real)
        if a.imag == 1:
            imag = "i"
        elif a.imag != 0:
            s = proper_str(a.imag)
            if s != "0":
                imag = proper_str(a.imag) + "i"
            else:
                imag = None
        else:
            imag = None
        if real == imag is None:
            return "0"
        return " + ".join(x for x in [real, imag] if x)

    if abs(a) == float("inf"):
        return str(a)

    if abs(a) > 1e15 and int(float(a)) == a:
        a = float(a)
    elif is_int(a):
        return str(round(a))

    if "e" in str(a):
        sig, exp = str(a).split("e")

        if int(exp) > 15 or int(exp) < -4:
            return str(sig) + "e" + str(int(exp))

    return str(a)


def check_type(obj: Any, typ: str) -> bool:
    if typ == "Number":
        return is_num(obj)

    if typ == "Integer":
        return is_int(obj)

    if typ == "Real":
        return is_real(obj)

    if typ == "String":
        return type(obj) == str

    if typ == "Any":
        return True

    if typ.startswith("Function"):
        return callable(obj)

    if typ.startswith("List"):
        return type(obj) == list

    raise ValueError("unknown type %s" % typ)


