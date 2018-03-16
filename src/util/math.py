# -*- coding: utf-8 -*-

import numbers


def isclose(a, b, rel_tol=1e-5, abs_tol=1e-8):
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
    if type(a) == complex or type(b) == complex:
        a = complex(a)
        b = complex(b)

    if type(a) == complex and type(b) == complex:
        return isclose(a.real, b.real) and isclose(a.imag, b.imag)

    if a == float("inf") and b != float("inf") or a != float("inf") and b == float("inf"):
        return False

    # if Python already considers the numbers to be identical, no need to waste CPU cycles for that
    if a == b:
        return True

    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def isnum(a):
    """Checks if the specified Python object is a number (int, float, long, etc)."""
    return isinstance(a, numbers.Number)


def isbool(a):
    """Checks if the specified Python object is a boolean."""
    return type(a) == bool


def isreal(a):
    """Checks if the specified complex number is real (imaginary part is zero)."""
    if not isnum(a):
        return False

    if type(a) != complex:
        return True

    return iszero(a.imag)


def isint(a):
    """Checks if the specified float is integral."""
    if type(a) == complex:
        return isreal(a) and isint(a.real)

    if not isnum(a) or abs(a) == float("inf"):
        return False

    return a == 0 or (1 <= a <= 1e15 and isclose(a, round(a)))


def iszero(a):
    if a == 0:
        return True

    if type(a) == complex:
        return iszero(a.real) and iszero(a.imag)

    if type(a) != float:
        return False

    if "e" in str(a):
        sig, exp = str(a).split("e")
        if isint(float(sig)):
            return False

    return isclose(a, 0)


def ispropnum(a):
    return isnum(a) and not isbool(a)


def propround(a, prec=None):
    if type(a) != float:
        return a

    if "e" not in str(a):
        return round(a, prec)

    sig, exp = str(a).split("e")

    return float("%se%s" % (round(float(sig), prec), exp))


def closeround(a, prec=None):
    if a is None:
        return 0

    if type(a) == complex:
        return complex(closeround(a.real, prec), closeround(a.imag, prec))

    if type(a) == int:
        return a

    if type(a) != float:
        return a

    if "e" in str(a):
        sig, exp = str(a).split("e")
        sig = float(sig)

        rnd = round(sig, prec)

        if isclose(rnd, sig):
            sig = rnd

        return float(str(sig) + "e" + exp)
    else:
        rnd = round(a, prec)

        if isclose(rnd, a):
            return rnd

    return a


def properstr(a):
    """Converts the specified float to string, removing comma if the number is integral."""
    if isbool(a):
        return "VRAI" if a else "FALSE"
    if type(a) == complex:
        rpart = None if iszero(a.real) else properstr(a.real)
        if a.imag == 1:
            cpart = "i"
        elif a.imag != 0:
            cpart = properstr(a.imag) + "i"
        else:
            cpart = None
        return " + ".join(x for x in [rpart, cpart] if x)
    if abs(a) > 1e15:
        a = float(a)
    elif isint(a):
        return str(round(a))
    if "e" in str(a):
        sig, exp = str(a).split("e")
        if int(exp) > 15:
            return str(sig) + "e" + str(int(exp))

    return str(a)
