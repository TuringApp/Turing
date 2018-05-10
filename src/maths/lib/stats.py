# -*- coding: utf-8 -*-

import builtins
import math
import random as rnd
import statistics

import numpy as np

from util import translate
from . import basic, trig
from .docs import *

__desc__ = translate("Docs", "Statistics")

doc_c("catalan", "G", "Catalan's constant")
c_catalan = 0.91596559417721901505460351493238411077414937428167

doc_c("glaisher", "A", "Glaisher-Kinkelin constant")
c_glaisher = 1.28242712910062263687534256886979172776768892732500


def listfunc(func):
    def wrapper(*args):
        if builtins.len(args) == 1:
            if isinstance(args[0], list):
                try:
                    return func(args[0])
                except:
                    pass

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


doc("erfinv",
    [
        ("y", "Number")
    ],
    translate("Docs", "Returns the inverse of the error function at {{y}}."))


def erfinv(y):
    # courtesy of
    # https://github.com/antelopeusersgroup/antelope_contrib/blob/master/lib/location/libgenloc/erfinv.c#L15
    a = [0.886226899, -1.645349621, 0.914624893, -0.140543331]
    b = [-2.118377725, 1.442710462, -0.329097515, 0.012229801]
    c = [-1.970840454, -1.624906493, 3.429567803, 1.641345311]
    d = [3.543889200, 1.637067800]
    if y > 1:
        return None
    if y == 1:
        return math.copysign(1, y) * float("inf")
    if y <= 0.7:
        z = y * y
        num = (((a[3] * z + a[2]) * z + a[1]) * z + a[0])
        dem = ((((b[3] * z + b[2]) * z + b[1]) * z + b[0]) * z + 1.0)
        x = y * num / dem
    else:
        z = math.sqrt(-math.log((1.0 - abs(y)) / 2.0))
        num = ((c[3] * z + c[2]) * z + c[1]) * z + c[0]
        dem = (d[1] * z + d[0]) * z + 1.0
        x = (math.copysign(1.0, y)) * num / dem
    for _ in [1, 2]:
        x = x - (erf(x) - y) / ((2 / math.sqrt(trig.c_pi)) * math.exp(-x * x))
    return x


doc("erfcinv",
    [
        ("y", "Number")
    ],
    translate("Docs", "Returns the inverse of the complementary error function at {{y}}."))


def erfcinv(y):
    return erfinv(1 - y)


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
    translate("Docs",
              "Returns the probability for {{k}} with the binomial distribution of parameters {{n}} and {{p}}."))


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
    translate("Docs",
              "Generates a list containing all number from {{start}} (inclusive) to {{end}} (exclusive) with a step of {{step}}."))


def range(start, end=None, step=None):
    if end is None:
        end = start
        start = 0
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
    translate("Docs",
              "Generates a list containing all number from {{start}} (inclusive) to {{end}} (inclusive) with a step of {{step}}."))


def irange(start, end=None, step=None):
    if end is None:
        end = start
        start = 0
    if step is None:
        if end < start:
            step = -1
        else:
            step = 1
    return np.arange(start, end + step, step)


doc("d_normal_pdf",
    [
        ("mu", "Real"),
        ("sigma", "Real"),
        ("x", "Real")
    ],
    translate("Docs",
              "Returns the probability for {{x}} with the normal distribution of parameters µ={{mu}} and σ={{sigma}}."))


def d_normal_pdf(mu, sigma, x):
    return 1 / (sigma * math.sqrt(2 * trig.c_pi)) * math.exp(
        - (math.pow(x - mu, 2) / (2 * math.pow(sigma, 2))))


doc("d_normal_std_pdf",
    [
        ("x", "Real")
    ],
    translate("Docs", "Returns the probability for {{x}} with the standard normal distribution (µ=0 and σ=1)."))


def d_normal_std_pdf(x):
    return 1 / math.sqrt(2 * trig.c_pi) * math.exp(-pow(x, 2) / 2)


doc("d_normal_cdf",
    [
        ("mu", "Real"),
        ("sigma", "Real"),
        ("x", "Real")
    ],
    translate("Docs",
              "Returns the cumulative probability for {{x}} with the normal distribution of parameters µ={{mu}} and σ={{sigma}}."))


def d_normal_cdf(mu, sigma, x):
    return d_normal_std_cdf((x - mu) / sigma)


doc("d_normal_std_cdf",
    [
        ("x", "Real")
    ],
    translate("Docs",
              "Returns the cumulative probability for {{x}} with the standard normal distribution (µ=0 and σ=1)."))


def d_normal_std_cdf(x):
    return 1 - 0.5 * erfc(x / math.sqrt(2))


doc("d_normal_cdf_inv",
    [
        ("mu", "Real"),
        ("sigma", "Real"),
        ("p", "Real")
    ],
    translate("Docs",
              "Returns the number with cumulative probability {{p}} with the normal distribution of parameters µ={{mu}} and σ={{sigma}}."))


def d_normal_cdf_inv(mu, sigma, p):
    return d_normal_std_cdf_inv(p) * sigma + mu


doc("d_normal_std_cdf_inv",
    [
        ("p", "Real")
    ],
    translate("Docs",
              "Returns the number with cumulative probability {{p}} with the standard normal distribution (µ=0 and σ=1)."))


def d_normal_std_cdf_inv(p):
    return erfcinv((1 - p) * 2) * math.sqrt(2)
