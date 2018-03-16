# -*- coding: utf-8 -*-

__desc__ = "Geometry"

import math
from .docs import *
from maths.lib import trig

doc("peri_circle",
    [
        ("radius", "Real")
    ],
    "Returns the perimeter of the circle with the specified {{radius}}.")


def peri_circle(radius):
    return 2 * trig.c_pi * radius


doc("area_triangle_sides",
    [
        ("a", "Real"),
        ("b", "Real"),
        ("c", "Real")
    ],
    "Returns the area of the triangle with the specified side lengths.")


def area_triangle_sides(a, b, c):
    p = (a + b + c) / 2.0
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


doc("area_triangle",
    [
        ("base", "Real"),
        ("height", "Real")
    ],
    "Returns the area of the triangle with the specified base and height.")


def area_triangle(base, height):
    return base * height / 2.0


doc("area_square",
    [
        ("side", "Real")
    ],
    "Returns the area of the square with the specified {{side}} length.")


def area_square(side):
    return side * side


doc("area_rectangle",
    [
        ("s1", "Real"),
        ("s2", "Real")
    ],
    "Returns the area of the rectangle with side lengths {{s1}} and {{s2}}.")


def area_rectangle(s1, s2):
    return s1 * s2


doc("area_trapezoid",
    [
        ("a", "Real"),
        ("b", "Real"),
        ("height", "Real")
    ],
    "Returns the area of the trapezoid with sides {{a}} and {{b}} and height {{height}}.")


def area_trapezoid(a, b, height):
    return (a + b) * height / 2.0


doc("area_circle",
    [
        ("radius", "Real")
    ],
    "Returns the area of the circle with the specified {{radius}}.")


def area_circle(radius):
    return math.pi * radius * radius


doc("area_ellipse",
    [
        ("r1", "Real"),
        ("r2", "Real")
    ],
    "Returns the area of the ellipse with radii {{r1}} and {{r2}}.")


def area_ellipse(r1, r2):
    return math.pi * r1 * r2


doc("area_parallelogram",
    [
        ("base", "Real"),
        ("height", "Real")
    ],
    "Returns the area of the parallelogram with the specified {{base}} and {{height}}.")


def area_parallelogram(base, height):
    return base * height


doc("area_sector",
    [
        ("radius", "Real"),
        ("angle", "Real")
    ],
    "Returns the area of the circle sector with the specified {{radius}} and {{angle}}.")


def area_sector(radius, angle):
    return (angle / 2) * radius * radius


doc("area_polygon",
    [
        ("sides", "Integer"),
        ("length", "Real")
    ],
    "Returns the area of the regular polygon with the specified number of {{sides}} and side {{length}}.")


def area_polygon(sides, length):
    return (sides * length * length) / (4 * math.tan(trig.c_pi / sides))


doc("area_sphere",
    [
        ("radius", "Real")
    ],
    "Returns the surface area of the sphere with the specified {{radius}}.")


def area_sphere(radius):
    return 4 * trig.c_pi * radius * radius


doc("area_cube",
    [
        ("side", "Real")
    ],
    "Returns the surface area of the cube with the specified {{side}} length.")


def area_cube(side):
    return 6 * side * side


doc("area_parallelepiped",
    [
        ("a", "Real"),
        ("b", "Real"),
        ("c", "Real")
    ],
    "Returns the surface area of the parallelogram with side lengths {{a}}, {{b}} and {{c}}.")


def area_parallelepiped(a, b, c):
    return (2 * a * b) + (2 * b * c) + (2 * a * c)


doc("area_cylinder",
    [
        ("radius", "Real"),
        ("height", "Real")
    ],
    "Returns the surface area of the cylinder with the specified {{radius}} and {{height}}.")


def area_cylinder(radius, height):
    return 2 * area_circle(radius) + height * peri_circle(radius)


doc("vol_pyramid",
    [
        ("sides", "Integer"),
        ("length", "Real"),
        ("height", "Real")
    ],
    "Returns the volume of the regular pyramid with the specified number of {{sides}}, side {{length}} and {{height}}.")


def vol_pyramid(sides, length, height):
    return area_polygon(sides, length) * height / 3


doc("vol_cube",
    [
        ("side", "Real")
    ],
    "Returns the volume of the cube with the specified {{side}} length.")


def vol_cube(side):
    return pow(side, 3)


doc("vol_sphere",
    [
        ("radius", "Real")
    ],
    "Returns the volume of the sphere with the specified {{radius}}.")


def vol_sphere(radius):
    return 4 * math.pi * pow(radius, 3) / 3


doc("vol_parallelepiped",
    [
        ("a", "Real"),
        ("b", "Real"),
        ("c", "Real")
    ],
    "Returns the volume of the parallelogram with side lengths {{a}}, {{b}} and {{c}}.")


def vol_parallellepiped(a, b, c):
    return a * b * c


doc("vol_cylinder",
    [
        ("radius", "Real"),
        ("height", "Real")
    ],
    "Returns the volume of the cylinder with the specified {{radius}} and {{height}}.")


def vol_cylinder(radius, height):
    return area_circle(radius) * height
