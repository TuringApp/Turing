# -*- coding: utf-8 -*-

import math
from .docs import *
import util

translate = util.translate

__desc__ = translate("Docs", "Other constants")

doc_c("e", "e", "Euler number")
c_e = 2.71828182845904523536028747135266249775724709369996

doc_c("phi", "φ", "Golden ratio")
c_phi = 1.61803398874989484820458683436563811772030917980576

doc_c("euler_gamma", "γ", "Euler-Mascheroni constant")
c_euler_gamma = 0.57721566490153286060651209008240243104215933593992

doc_c("khinchin", "K<sub>0</sub>", "Khinchin's constant")
c_khinchin = 2.68545200106530644530971483548179569382038229399446

doc_c("inf", "∞", "Positive infinity")
c_inf = complex("inf")

doc_c("i", "i", "Imaginary unit")
c_i = complex(0, 1)
