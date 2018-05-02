# -*- coding: utf-8 -*-
from maths.lib.basic import *
from maths.lib.stats import *
from util import translate

__desc__ = translate("Docs", "Algobox compatibility")

ALGOBOX_ALEA_ENT = randint
ALGOBOX_NB_COMBINAISONS = binomial
ALGOBOX_COEFF_BINOMIAL = binomial
ALGOBOX_LOI_BINOMIAL = d_binomial
ALGOBOX_LOI_NORMALE_CR = None
ALGOBOX_LOI_NORMALE = None
ALGOBOX_INVERSE_LOI_NORMALE_CR = None
ALGOBOX_INVERSE_LOI_NORMALE = None
ALGOBOX_FACTORIELLE = fact
ALGOBOX_SOMME = lambda lst, p, n: sum(lst[p:n + 1])
ALGOBOX_MOYENNE = lambda lst, p, n: arithm_mean(lst[p:n + 1])
ALGOBOX_VARIANCE = lambda lst, p, n: variance(lst[p:n + 1])
ALGOBOX_ECART_TYPE = lambda lst, p, n: stand_dev(lst[p:n + 1])
ALGOBOX_MEDIANE = median
ALGOBOX_QUARTILE1 = None
ALGOBOX_QUARTILE3 = None
ALGOBOX_QUARTILE1_BIS = None
ALGOBOX_QUARTILE3_BIS = None
ALGOBOX_MINIMUM = lambda lst, p, n: min(lst[p:n + 1])
ALGOBOX_MAXIMUM = lambda lst, p, n: max(lst[p:n + 1])
ALGOBOX_POS_MINIMUM = lambda lst, p, n: lst[p:n + 1].index(ALGOBOX_MINIMUM(lst, p, n))
ALGOBOX_POS_MAXIMUM = lambda lst, p, n: lst[p:n + 1].index(ALGOBOX_MAXIMUM(lst, p, n))
ALGOBOX_ARRONDIR = round
