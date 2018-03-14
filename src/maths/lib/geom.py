# -*- coding: utf-8 -*-

import math

def peri_circle(radius):
	return 2 * math.pi * radius

def area_triangle_sides(a, b, c):
	p = (a + b + c) / 2.0
	return sqrt(p * (p - a) * (p - b) * (p - c))

def area_triangle(base, height):
	return base * height / 2.0

def area_square(side):
	return side * side

def area_rectangle(s1, s2):
	return s1 * s2

def area_trapezoid(a, b, height):
	return (a + b) * height / 2.0

def area_circle(radius):
	return math.pi * radius * radius

def area_ellipse(r1, r2):
	return math.pi * r1 * r2

def area_parallelogram(base, height):
	return base * height

def area_sector(radius, angle):
	return (angle / 2) * radius * radius

def area_polygon(sides, length):
	return (sides * length * length) / (4 * tan(math.pi / sides))

def area_sphere(radius):
	return 4 * math.pi * radius * radius

def area_cube(side):
	return 6 * side * size

def area_parallelepiped(a, b, c):
	return (2 * a * b) + (2 * b * c) + (2 * a * c)

def area_cylinder(radius, height):
	return 2 * area_circle(radius) + height * peri_circle(radius)

def vol_pyramid(sides, length, height):
	return area_polygon(sides, length) * height / 3

def vol_cube(side):
	return pow(side, 3)

def vol_sphere(radius):
	return 4 * math.pi * pow(radius, 3) / 3

def vol_parallellepiped(a, b, c):
	return a * b * c

def vol_cylinder(radius, height):
	return area_circle(radius) * height