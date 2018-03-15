# -*- coding: utf-8 -*-

import maths.lib
import itertools
import re
from util.math import isint

cts = maths.lib.get_consts()

for k in sorted(cts.keys()):
	print("|&nbsp;|**%s**|&nbsp;|" % k)

	for c in sorted(cts[k], key=lambda x:x[0]):
		name, symbol, desc = c[:3]

		actual = getattr(maths.lib.get_modules()[k], "c_" + name)

		if isint(actual):
			# if integer, only value is needed
			val = str(actual)
		else:
			if "e" in str(actual):
				# if exponent, add pretty html
				sig, exp = str(actual).split("e")
				val = str(round(float(sig), 15)) + "&middot;10<sup>%d</sup>" % int(exp)
			else:
				# otherwise, only rounded value
				val = "%.15f" % actual

		unit = ""
		if len(c) > 3:
			# add unit
			unit = " (%s)" % c[3].replace("*", "&middot;")

		desc = re.sub(r"//(\w+)//", "*\g<1>*", f[2])

		print("|`%s`|%s|*%s* - %s%s|" % (name, val, symbol, desc, unit))