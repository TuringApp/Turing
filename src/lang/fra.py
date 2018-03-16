 # -*- coding: utf-8 -*-

__desc__ = "Traduction française"

doc("arrondi", 
	[
		("num", "Nombre"), 
		("prec", "Entier", None, None)
	], 
	"Arrondi {{num}} à l'entier le plus proche / (si spécifié) à {{prec}} décimales.",
	["round"])

doc("abs",
	[
		("num", "Nombre")
	],
	"Retourne la valeur absolue de {{num}}.")

doc("rac",
	[
		("num", "Nombre", ">= 0")
	],
	"Retourne la racine carré de {{num}}.",
	["sqrt"])

doc("root",
	[
		("num", "Number"),
		("n", "Number", "!= 0")
	],
	"Returns the {{n}}-th root of {{num}}.")

doc("pow",
	[
		("num", "Number"),
		("p", "Number")
	],
	"Returns {{num}} to the {{p}}-th power.",
	["puiss"])

doc("exp",
	[
		("num", "Number")
	],
	"Returns //e// to the power of {{num}}.")

doc("ln",
	[
		("num", "Number")
	],
	"Returns the natural (base-//e//) logarithm of {{num}}.")

doc("log",
	[
		("num", "Number"),
		("b", "Number", "!= 0", 10)
	],
	"Returns the base-{{b}} logarithm of {{num}}.")

doc("log10",
	[
		("num", "Number")
	],
	"Returns the base-10 logarithm of {{num}}.")

doc("floor",
	[
		("num", "Number")
	],
	"Returns the largest integer less than or equal to {{num}}.")

doc("ceil",
	[
		("num", "Number")
	],
	"Returns the smallest integer greater than or equal to {{num}}.")

doc("sign",
	[
		("num", "Number")
	],
	"Returns the sign of {{num}} (-1 if negative, 1 if positive, 0 otherwise).")

doc("gcd",
	[
		("a", "Integer"),
		("b", "Integer")
	],
	"Returns the greatest common divisor of {{a}} and {{b}}.",
	['pgcd'])

doc("lcm",
	[
		("a", "Integer"),
		("b", "Integer")
	],
	"Returns the least common multiple of {{a}} and {{b}}.",
	['ppcm'])