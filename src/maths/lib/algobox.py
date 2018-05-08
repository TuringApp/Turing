# -*- coding: utf-8 -*-
from maths.lib.basic import *
from maths.lib.stats import *
from util import translate

__desc__ = translate("Docs", "Algobox compatibility")

def algobox_listfunc(func):
    def wrapper(lst, p, n):
        return func(lst[p:n + 1])

    setattr(wrapper, "algobox_listfunc", True)
    return wrapper

ALGOBOX_ALEA_ENT = randint
ALGOBOX_NB_COMBINAISONS = binomial
ALGOBOX_COEFF_BINOMIAL = binomial
ALGOBOX_LOI_BINOMIAL = d_binomial
ALGOBOX_LOI_NORMALE_CR = None
ALGOBOX_LOI_NORMALE = None
ALGOBOX_INVERSE_LOI_NORMALE_CR = None
ALGOBOX_INVERSE_LOI_NORMALE = None
ALGOBOX_FACTORIELLE = fact
ALGOBOX_SOMME = algobox_listfunc(sum)
ALGOBOX_MOYENNE = algobox_listfunc(arithm_mean)
ALGOBOX_VARIANCE = algobox_listfunc(variance)
ALGOBOX_ECART_TYPE = algobox_listfunc(stand_dev)
ALGOBOX_MEDIANE = algobox_listfunc(median)
ALGOBOX_QUARTILE1 = None
ALGOBOX_QUARTILE3 = None
ALGOBOX_QUARTILE1_BIS = None
ALGOBOX_QUARTILE3_BIS = None
ALGOBOX_MINIMUM = algobox_listfunc(min)
ALGOBOX_MAXIMUM = algobox_listfunc(max)
ALGOBOX_POS_MINIMUM = algobox_listfunc(min_index)
ALGOBOX_POS_MAXIMUM = algobox_listfunc(max_index)
ALGOBOX_ARRONDIR = round
