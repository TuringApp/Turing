# -*- coding: utf-8 -*-

import numbers

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Checks if the specified numbers are close enough to be considered equal.

    Due to the usage of IEEE754 floating points number in Python, formulae like 0.1+0.2
    can lead to surprising results different from 0.3, for example 0.2999999999 and similar oddities.
    This function only compares the numbers up to a certain precision (by default 10^-9).

    a       -- first number
    b       -- second number
    rel_tol -- relative tolerance (number of digits)
    abs_tol -- absolute tolerance

    Note: this function was added in Python 3.5, thus this implementation is added to allow Turing to run on older versions."""

    # if only one of the two is Infinity, then they are not identical
    if a == float("inf") and b != float("inf") or a != float("inf") and b == float("inf"): 
        return False

    # if Python already considers the numbers to be identical, no need to waste CPU cycles for that
    if a == b:
        return True

    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def isnum(a):
    """Checks if the specified Python object is a number (int, float, long, etc)."""
    return isinstance(a, numbers.Number)

def isint(a):
    """Checks if the specified float is integral."""
    if not isnum(a) or abs(a) == float("inf"):
        return False

    return isclose(a, round(a))

def properstr(a):
    """Converts the specified float to string, removing comma if the number is integral."""
    if isint(a) and not isinstance(a, bool):
        return str(round(a))
    return str(a)