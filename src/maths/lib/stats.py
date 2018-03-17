# -*- coding: utf-8 -*-

import builtins
import math
import random as rnd
import statistics

import util
from maths.lib import basic
from .docs import *

translate = util.translate

__desc__ = translate("Docs", "Statistics")

doc_c("catalan", "G", "Catalan's constant")
c_catalan = 0.91596559417721901505460351493238411077414937428167

doc_c("glaisher", "A", "Glaisher-Kinkelin constant")
c_glaisher = 1.28242712910062263687534256886979172776768892732500

doc("arithm_mean",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the arithmetic mean of {{args}}."),
    ["moyenne", "average"])


def arithm_mean(args):
    return statistics.mean(args)


average = arithm_mean
moyenne = arithm_mean

doc("harmonic_mean",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the harmonic mean of {{args}}."),
    ["moyenne_harmo"])


def harmonic_mean(*args):
    if "harmonic_mean" not in dir(statistics):
        return len(args) / sum([1 / x for x in args])
    return statistics.harmonic_mean(args)


moyenne_harmo = harmonic_mean

doc("sum",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the sum of all the terms of {{args}}."))


def sum(args):
    return builtins.sum(args)


doc("binomial",
    [
        ("n", "Number"),
        ("k", "Number")
    ],
    translate("Docs", "Returns the binomial coefficient for a subset of size {{k}} and a set of size {{n}}."))


def binomial(n, k):
    """Calculates the binomial coefficient."""
    return math.gamma(n + 1) / (math.gamma(k + 1) * math.gamma(n - k + 1))


doc("max",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the maximum value of {{args}}."))


def max(*args):
    return builtins.max(args)


doc("min",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the minimum value of {{args}}."))


def min(args):
    return builtins.min(args)


doc("gamma",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the Gamma function at {{x}}."))


def gamma(x):
    return math.gamma(x)


doc("log_gamma",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the natural logarithm of the absolute value of the Gamma function at {{x}}."))


def log_gamma(x):
    return math.lgamma(x)


doc("fact",
    [
        ("x", "Integer")
    ],
    translate("Docs", "Returns the factorial of {{x}}."))


def fact(x):
    return math.factorial(x)


doc("erf",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the error function at {{x}}."))


def erf(x):
    return math.erf(x)


doc("erfc",
    [
        ("x", "Number")
    ],
    translate("Docs", "Returns the complementary error function at {{x}}."))


def erfc(x):
    return math.erfc(x)


doc("map",
    [
        ("func", "Function(1 arg)"),
        ("lst", "List")
    ],
    translate("Docs", "Applies {{func}} to each element of {{lst}} and returns the resulting list."),
    ["appl"])


def map(func, lst):
    return list(builtins.map(func, lst))


appl = map

doc("filter",
    [
        ("func", "Function(1 arg)"),
        ("lst", "List")
    ],
    translate("Docs", "Returns a list containing all elements of {{lst}} for which {{func}} returns a truthy value."),
    ["filtre"])


def filter(func, lst):
    return list(builtins.filter(func, lst))


filtre = filter

doc("slice",
    [
        ("lst", "List"),
        ("start", "Integer", "0 <= start <= end <= len(lst)"),
        ("end", "Integer", "start <= end <= len(lst)", None)
    ],
    translate("Docs",
              "Returns a slice of the specified list, from index {{start}} (inclusive) to either index "
              "{{end}} (exclusive) or the end of the list."),
    ["tranche"])


def slice(lst, start, end=None):
    start = int(start)
    if end is not None:
        end = int(end)
        return lst[start:end]
    return lst[start:]


tranche = slice

doc("stand_dev",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the population standard deviation of {{lst}}."),
    ["ecart_type"])


def stand_dev(lst):
    return statistics.pstdev(lst)


ecart_type = stand_dev

doc("variance",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the population variance of {{lst}}."))


def variance(lst):
    return statistics.pvariance(lst)


doc("stand_dev_sample",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the sample standard deviation of {{lst}}."),
    ["ecart_type_echant"])


def stand_dev_sample(lst):
    return statistics.stdev(lst)


ecart_type_echant = stand_dev_sample

doc("variance_sample",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the sample variance of {{lst}}."),
    ["variance_echant"])


def variance_sample(lst):
    return statistics.variance(lst)


variance_echant = variance_sample

doc("random",
    [],
    translate("Docs", "Returns a random number between 0 (inclusive) and 1 (exclusive)."),
    ["alea"])


def random():
    return rnd.random()


alea = random

doc("fib",
    [
        ("n", "Integer")
    ],
    translate("Docs", "Returns the {{n}}-th Fibonacci number."))


def fib(n):
    a, b = 1, 1
    for i in range(int(n) - 1):
        a, b = b, a + b
    return a


doc("euler",
    [
        ("n", "Integer")
    ],
    translate("Docs", "Returns the {{n}}-th Euler number."))


def euler(n):
    # odd indices are zero
    if int(n) % 2 != 0:
        return 0

    n = int(n / 2)
    return basic.pow(-1, n) \
           * complex(0, 1) \
           * sum(sum(binomial(k, j)
                     * ((basic.pow(-1, j) * basic.pow(k - 2 * j, 2 * n + 1)) / (
            basic.pow(2, k) * basic.pow(complex(0, 1), k) * k))
                     for j in range(0, k + 1)
                     )
                 for k in range(1, 2 * n + 2)
                 )


doc("beta",
    [
        ("a", "Number"),
        ("b", "Number")
    ],
    translate("Docs", "Returns the Beta function at {{a}} and {{b}}."))


def beta(a, b):
    return (gamma(a) * gamma(b)) / gamma(a + b)
