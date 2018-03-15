# -*- coding: utf-8 -*-

import maths.lib
import itertools
import re

fns = maths.lib.get_funcs()

for k in sorted(fns.keys()):
	print("|&nbsp;|**%s**|&nbsp;|" % k)

	for f in sorted(fns[k], key=lambda x:x[0]):
		names = [f[0]]

		if len(f) > 3:
			# add alias
			names = names + f[3] 

		name = " / ".join("`%s`" % x for x in names)

		# check if any parameters
		if f[1]: 
			args = "<ul>"
			for arg in f[1]:
				args += "<li>"
				args += "`%s` (%s)" % (arg[0], arg[1])
				if len(arg) > 2:
					constr = arg[2]
					if len(arg) > 3:
						deft = "default = %s" % arg[3] if arg[3] != None else None
					else:
						deft = None
					infos = ", ".join(x for x in [constr, deft] if x)
					if infos:
						args += " " + infos
				args += "</li>"
			args += "</ul>"

		# replace {{x}} by `x` for markdown
		desc = re.sub(r"\{\{(\w+)\}\}", "`\g<1>`", f[2])
		desc = re.sub(r"//(\w+)//", "*\g<1>*", f[2])

		print("|%s|%s|%s|" % (name, args, desc))

