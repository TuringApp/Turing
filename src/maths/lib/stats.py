# -*- coding: utf-8 -*-

import builtins
import math
import random as rnd
import statistics
import numpy as np

from maths.lib import basic
from util import translate
from .docs import *

__desc__ = translate("Docs", "Statistics")

doc_c("catalan", "G", "Catalan's constant")
c_catalan = 0.91596559417721901505460351493238411077414937428167

doc_c("glaisher", "A", "Glaisher-Kinkelin constant")
c_glaisher = 1.28242712910062263687534256886979172776768892732500

def listfunc(func):
    def wrapper(*args):
        if builtins.len(args) == 1:
            try:
                if isinstance(args[0], list):
                    return func(args[0])
            except:
                try:
                    return func(list(iter(args[0])))
                except:
                    pass
        return func(list(args))
    setattr(wrapper, "listfunc", True)
    return wrapper

doc("arithm_mean",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the arithmetic mean of {{args}}."),
    ["moyenne", "average"])


@listfunc
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


@listfunc
def harmonic_mean(args):
    if "harmonic_mean" not in dir(statistics):
        return builtins.len(args) / sum([1 / x for x in args])
    return statistics.harmonic_mean(args)


moyenne_harmo = harmonic_mean

doc("sum",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the sum of all the terms of {{args}}."))


@listfunc
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


@listfunc
def max(args):
    return builtins.max(args)


doc("min",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the minimum value of {{args}}."))


@listfunc
def min(args):
    return builtins.min(args)


doc("max_index",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the index of maximum value of {{args}}."))


@listfunc
def max_index(args):
    return args.index(builtins.max(args))


doc("min_index",
    [
        ("args", "List(Number)")
    ],
    translate("Docs", "Returns the index of minimum value of {{args}}."))


@listfunc
def min_index(args):
    return args.index(builtins.min(args))


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
    return [func(x) for x in lst]


appl = map

doc("filter",
    [
        ("func", "Function(1 arg)"),
        ("lst", "List")
    ],
    translate("Docs", "Returns a list containing all elements of {{lst}} for which {{func}} returns a truthy value."),
    ["filtre"])


def filter(func, lst):
    return [x for x in lst if func(x)]


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


@listfunc
def stand_dev(lst):
    return statistics.pstdev(lst)


ecart_type = stand_dev

doc("variance",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the population variance of {{lst}}."))


@listfunc
def variance(lst):
    return statistics.pvariance(lst)


doc("stand_dev_sample",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the sample standard deviation of {{lst}}."),
    ["ecart_type_echant"])


@listfunc
def stand_dev_sample(lst):
    return statistics.stdev(lst)


ecart_type_echant = stand_dev_sample

doc("variance_sample",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the sample variance of {{lst}}."),
    ["variance_echant"])


@listfunc
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

doc("randint",
    [
        ("a", "Integer"),
        ("b", "Integer")
    ],
    translate("Docs", "Returns a random integer between {{a}} and {{b}} (inclusive)."),
    ["alea_ent"])


def randint(a, b):
    if b < a:
        a, b = b, a

    return math.floor((b - a + 1) * random() + a)


alea_ent = randint

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


doc("median",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the median of {{lst}}."))


@listfunc
def median(lst):
    return statistics.median(lst)


doc("mode",
    [
        ("lst", "List(Number)"),
    ],
    translate("Docs", "Returns the mode of {{lst}}."))


@listfunc
def mode(lst):
    return statistics.mode(lst)


doc("d_binomial",
    [
        ("n", "Integer"),
        ("p", "Real", "0 <= p <= 1"),
        ("k", "Integer")
    ],
    translate("Docs", "Returns the probability for {{k}} with the binomial distribution of parameters {{n}} and {{p}}."))


@listfunc
def d_binomial(n, p, k):
    return binomial(n, k) * basic.pow(p, k) * basic.pow(1 - p, n - k)


doc("len",
    [
        ("T", "List")
    ],
    translate("Docs", "Returns the number of elements in {{T}}."),
    ["taille"])


@listfunc
def len(T):
    return builtins.len(T)

taille = len

doc("swap",
    [
        ("T", "List"),
        ("a", "Integer"),
        ("b", "Integer")
    ],
    translate("Docs", "Swaps the elements of {{t}} at indices {{a}} and {{b}}."))


def swap(T, a, b):
    T[a], T[b] = T[b], T[a]
    return T


doc("range",
    [
        ("start", "Number"),
        ("end", "Number"),
        ("step", "Number", None, 1)
    ],
    translate("Docs", "Generates a list containing all number from {{start}} (inclusive) to {{end}} (exclusive) with a step of {{step}}."))


def range(start, end, step=None):
    if step is None:
        if end < start:
            step = -1
        else:
            step = 1
    return np.arange(start, end, step)


doc("irange",
    [
        ("start", "Number"),
        ("end", "Number"),
        ("step", "Number", None, 1)
    ],
    translate("Docs", "Generates a list containing all number from {{start}} (inclusive) to {{end}} (inclusive) with a step of {{step}}."))


def irange(start, end, step=None):
    if step is None:
        if end < start:
            step = -1
        else:
            step = 1
    return np.arange(start, end + step, step)