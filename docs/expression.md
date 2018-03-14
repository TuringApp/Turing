# Built-in expression parser

Turing has a built-in mathematical expression parser, which is used when the program is in pseudocode mode.

The language is case-insensitive for keywords, i.e. `FALSE`, `false` and `FaLsE` are the same thing.

## Types

### Number

Stored using a Python `float`, automatically converted to `int` when needed.

A point (`.`) shall be used to separate the integer part from the fractional part.

#### Example

- `42`
- `3.1415`

### Boolean

Stored using a Python `bool`, automatically converted to Number when needed (only if strict mode is disabled).

#### Syntax

The following keywords are available:
- `TRUE` / `VRAI` : True value
- `FALSE` / `FAUX` : False value

### String

Stored using a Python `str` (Unicode).

A string is enclosed between double quotes (`"`). It is not possible yet to escape characters inside a string literal.

### List

Stored using a Python `list`, indices start at 0 (like in any real programming language. *Lua*, you should feel ashamed of yourself).

#### Operators

Certain operators can be applied on operands of type List.

##### `+` (Plus)

Concatenates two lists.

###### Examples

- `[1, 2, 3] + [3, 4, 5] == [1, 2, 3, 3, 4, 5]`

##### `-` (Binary minus)

Returns all items of A that are not in B.

###### Examples

- `[1, 2, 3] - [3, 4, 5] == [1, 2]`

##### `-` (Unary minus)

Returns a reversed copy of the list.

###### Examples

- `-[1, 2, 3] == [3, 2, 1]`

##### `*` (Times)

*Must be used on a List and a Number together.*

Duplicates the list the specified amount of times.

###### Examples

- `[1, 2, 3] * 3 == [1, 2, 3, 1, 2, 3, 1, 2, 3]`

##### `&` / `ET` (Intersection)

Returns all items of A that are also in B.

###### Examples

- `[1, 2, 3] & [2, 3, 4] == [2, 3]`

##### `|` / `OU` (Union)

Returns an ordered list of all items of A and all items of B, without duplicates.

###### Examples

- `[1, 2, 3] | [2, 3, 4] == [1, 2, 3, 4]`

##### `XOR` (exclusive Or)

Returns an ordered list of all items that are present either in A or B but not both.

###### Examples

- `[1, 2, 3] XOR [3, 4, 5] == [1, 2, 4, 5]`

### Function / lambda

Standard Python function.

#### Lambda/inline function syntax

Comma-separated list of parameters enclosed in braces, followed by expression enclosed in parentheses. The function can be called immediately. There is no limit to the amount of parameters. A parameter is made of an identifier, no less, no more.

Varargs are not available yet.

##### Examples

- `{x, y}(2 * x + y)(3, 8) == 14`
- `map({a}(2 * a), [2, 3, 4]) == [4, 6, 8]`

## Operators

### Binary operators

| Symbol | Operator | Types |
|--------|----------|-------|
| `+` | Plus, Concatenate | Number, String, List |
| `-` | Minus, Reverse | Number, List |
| `*` | Times, Repeat | Number, List |
| `/` | Divide | Number |
| `%` | Modulus | Number |
| `^` | Power | Number |
| `<=` | Less than or equal | Number |
| `<` | Strictly less than | Number |
| `>` | Strictly greater than | Number |
| `>=` | Greater than or equal | Number |
| `==` | Equals | All |
| `!=` | Not equals | All |
| `&` / `ET` | AND / Intersection | Number, Boolean, List |
| <code>&#124;</code> / `OU` | OR / Union | Number, Boolean, List |
| `XOR` | Exclusive OR / Exclusive union | Number, Boolean, List |

### Unary operators

| Symbol | Operator | Types |
|--------|----------|-------|
| `-` | Negate | Number, List |
| `NON` | Invert | Boolean |

The numbers and booleans are treated the same way as in **plain Python**. In other words, booleans can be treated as numbers (`False` becomes 0 and `True` becomes 1), and numbers can be treated as booleans (0 becomes `False` and everything else becomes `True).

If **strict mode** is enabled, operators can only be used with operands of **identical type**, and **implicit number-boolean casts** are disabled. The `c_bool` and `c_num` functions can then be used for that purpose.

## Function library

The engine provides many functions that can be used with almost all value types.

In the following table, a type name followed by a star (*) means that the function accepts a variable argument list of the specified type.

#### Example

The `average` function accepts either List(Number) or Number*. Thus, it can be used either with a list object: `average(myList)` or with varargs: `average(1, 2, 3)`.

| Name | Parameters | Description |
|------|------------|-------------|
|&nbsp;|**Basic**|&nbsp;|
|`abs`|<ul><li>`num` (Number)</li></ul>|Returns the absolute value of `num`.|
|`abs` / `rac`|<ul><li>`num` (Number) >= 0</li></ul>|Returns the square root of `num`.|
|`ceil`|<ul><li>`num` (Number)</li></ul>|Returns the smallest integer greater than or equal to `num`.|
|`exp`|<ul><li>`num` (Number)</li></ul>|Returns *e* to the power of `num`.|
|`floor`|<ul><li>`num` (Number)</li></ul>|Returns the largest integer less than or equal to `num`.|
|`gcd`|<ul><li>`a` (Integer)</li><li>`b` (Integer)</li></ul>|Returns the greatest common divisor of `a` and `b`.|
|`ln`|<ul><li>`num` (Number)</li></ul>|Returns the natural (base-*e*) logarithm of `num`.|
|`log`|<ul><li>`num` (Number)</li><li>`b` (Number) != 0, default = 10</li></ul>|Returns the base-`b` logarithm of `num`.|
|`log10`|<ul><li>`num` (Number)</li></ul>|Returns the base-10 logarithm of `num`.|
|`pow` / `puiss`|<ul><li>`num` (Number)</li><li>`p` (Number)</li></ul>|Returns `num` to the `p`-th power.|
|`root`|<ul><li>`num` (Number)</li><li>`n` (Number) != 0</li></ul>|Returns the `n`-th root of `num`.|
|`round` / `arrondi`|<ul><li>`num` (Number)</li><li>`prec` (Integer)</li></ul>|Rounds `num` to the nearest integer / (if specified) to `prec` decimals.|
|`sign`|<ul><li>`num` (Number)</li></ul>|Returns the sign of `num` (-1 if negative, 1 if positive, 0 otherwise).|
|&nbsp;|**Geometry**|&nbsp;|
|`area_circle`|<ul><li>`radius` (Number)</li></ul>|Returns the area of the circle with the specified `radius`.|
|`area_cube`|<ul><li>`side` (Number)</li></ul>|Returns the surface area of the cube with the specified `side` length.|
|`area_cylinder`|<ul><li>`radius` (Number)</li><li>`height` (Number)</li></ul>|Returns the surface area of the cylinder with the specified `radius` and `height`.|
|`area_ellipse`|<ul><li>`r1` (Number)</li><li>`r2` (Number)</li></ul>|Returns the area of the ellipse with radii `r1` and `r2`.|
|`area_parallelepiped`|<ul><li>`a` (Number)</li><li>`b` (Number)</li><li>`c` (Number)</li></ul>|Returns the surface area of the parallelogram with side lengths `a`, `b` and `c`.|
|`area_parallelogram`|<ul><li>`base` (Number)</li><li>`height` (Number)</li></ul>|Returns the area of the parallelogram with the specified `base` and `height`.|
|`area_polygon`|<ul><li>`sides` (Integer)</li><li>`length` (Number)</li></ul>|Returns the area of the regular polygon with the specified number of `sides` and side `length`.|
|`area_rectangle`|<ul><li>`s1` (Number)</li><li>`s2` (Number)</li></ul>|Returns the area of the rectangle with side lengths `s1` and `s2`.|
|`area_sector`|<ul><li>`radius` (Number)</li><li>`angle` (Number)</li></ul>|Returns the area of the circle sector with the specified `radius` and `angle`.|
|`area_sphere`|<ul><li>`radius` (Number)</li></ul>|Returns the surface area of the sphere with the specified `radius`.|
|`area_square`|<ul><li>`side` (Number)</li></ul>|Returns the area of the square with the specified `side` length.|
|`area_trapzeoid`|<ul><li>`a` (Number)</li><li>`b` (Number)</li><li>`height` (Number)</li></ul>|Returns the area of the trapezoid with sides `a` and `b` and height `height`.|
|`area_triangle`|<ul><li>`base` (Number)</li><li>`height` (Number)</li></ul>|Returns the area of the triangle with the specified base and height.|
|`area_triangle_sides`|<ul><li>`a` (Number)</li><li>`b` (Number)</li><li>`c` (Number)</li></ul>|Returns the area of the triangle with the specified side lengths.|
|`peri_circle`|<ul><li>`radius` (Number)</li></ul>|Returns the perimeter of the circle with the specified `radius`.|
|`vol_cube`|<ul><li>`side` (Number)</li></ul>|Returns the volume of the cube with the specified `side` length.|
|`vol_cylinder`|<ul><li>`radius` (Number)</li><li>`height` (Number)</li></ul>|Returns the volume of the cylinder with the specified `radius` and `height`.|
|`vol_parallelepiped`|<ul><li>`a` (Number)</li><li>`b` (Number)</li><li>`c` (Number)</li></ul>|Returns the volume of the parallelogram with side lengths `a`, `b` and `c`.|
|`vol_pyramid`|<ul><li>`sides` (Integer)</li><li>`length` (Number)</li><li>`height` (Number)</li></ul>|Returns the volume of the regular pyramid with the specified number of `sides`, side `length` and `height`.|
|`vol_sphere`|<ul><li>`radius` (Number)</li></ul>|Returns the volume of the sphere with the specified `radius`.|
|&nbsp;|**Statistics**|&nbsp;|
|`average` / `moyenne`|<ul><li>`args` (List(Number) / Number*)</li></ul>|Returns the arithmetic mean of `args`.|
|`binomial`|<ul><li>`n` (Number)</li><li>`k` (Number)</li></ul>|Returns the binomial coefficient for a subset of size `k` and a set of size `n`.|
|`erf`|<ul><li>`x` (Number)</li></ul>|Returns the error function at `x`.|
|`erfc`|<ul><li>`x` (Number)</li></ul>|Returns the complementary error function at `x`.|
|`fact`|<ul><li>`x` (Integer)</li></ul>|Returns the factorial of `x`.|
|`filter` / `filtre`|<ul><li>`func` (Function(1 arg))</li><li>`lst` (List)</li></ul>|Returns a list containing all elements of `lst` for which `func` returns a truthy value.|
|`gamma`|<ul><li>`x` (Number)</li></ul>|Returns the Gamma function at `x`.|
|`map` / `appl`|<ul><li>`func` (Function(1 arg))</li><li>`lst` (List)</li></ul>|Applies `func` to each element of `lst` and returns the resulting list.|
|`max`|<ul><li>`args` (List(Number) / Number*)</li></ul>|Returns the maximum value of `args`.|
|`min`|<ul><li>`args` (List(Number) / Number*)</li></ul>|Returns the minimum value of `args`.|
|`sum`|<ul><li>`args` (List(Number) / Number*)</li></ul>|Returns the sum of all the terms of `args`.|
|&nbsp;|**Trigonometry**|&nbsp;|
|`acos`|<ul><li>`x` (Number)</li></ul>|Returns the arc cosine of `x`.|
|`acosh`|<ul><li>`x` (Number)</li></ul>|Returns the inverse hyperbolic cosine of `x`.|
|`asin`|<ul><li>`x` (Number)</li></ul>|Returns the arc sine of `x`.|
|`asinh`|<ul><li>`x` (Number)</li></ul>|Returns the inverse hyperbolic sine of `x`.|
|`atan`|<ul><li>`x` (Number)</li></ul>|Returns the arc tangent of `x`.|
|`atan2`|<ul><li>`x` (Number)</li><li>`y` (Number)</li></ul>|Returns the arc tangent of `y` / `x`.|
|`atanh`|<ul><li>`x` (Number)</li></ul>|Returns the inverse hyperbolic tangent of `x`.|
|`cos`|<ul><li>`x` (Number)</li></ul>|Returns the cosine of `x`.|
|`cosh`|<ul><li>`x` (Number)</li></ul>|Returns the hyperbolic cosine of `x`.|
|`degrees` / `deg`|<ul><li>`x` (Number)</li></ul>|Converts angle `x` from radians to degrees.|
|`radians` / `rad`|<ul><li>`x` (Number)</li></ul>|Converts angle `x` from degrees to radians.|
|`sin`|<ul><li>`x` (Number)</li></ul>|Returns the sine of `x`.|
|`sinh`|<ul><li>`x` (Number)</li></ul>|Returns the hyperbolic sine of `x`.|
|`tan`|<ul><li>`x` (Number)</li></ul>|Returns the tangent of `x`.|
|`tanh`|<ul><li>`x` (Number)</li></ul>|Returns the hyperbolic tangent of `x`.|
|&nbsp;|**Type conversion**|&nbsp;|
|`c_bool`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to Boolean.|
|`c_list`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to List.|
|`c_num`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to Number.|
|`c_str`|<ul><li>`obj` (Any)</li></ul>|Converts `obj` to String.|

Useful (?) constants are also provided, with the maximum supported precision.

| Name | Approximated value | Description |
|------|-------------------:|-------------|
|&nbsp;|**Other constants**|&nbsp;|
|`e`|2.718281828459045|*e* - Euler number|
|`euler_gamma`|0.577215664901533|*γ* - Euler-Mascheroni constant|
|`inf`|inf|*∞* - Positive infinity|
|`khinchin`|2.685452001065306|*K<sub>0</sub>* - Khinchin's constant|
|`phi`|1.618033988749895|*φ* - Golden ratio|
|&nbsp;|**Physics**|&nbsp;|
|`celerity`|299792458|*c* - Speed of light in vacuum (m&middot;s<sup>-1</sup>)|
|`gravity`|6.6740831&middot;10<sup>-11</sup>|*G* - Gravitational constant (N&middot;m<sup>2</sup>&middot;kg<sup>-2</sup>)|
|`planck`|6.62607004081&middot;10<sup>-34</sup>|*h* - Planck constant (J&middot;s<sup>-1</sup>)|
|`planck_charge`|1.8755459&middot;10<sup>-18</sup>|*q<sub>P</sub>* - Planck charge (C)|
|`planck_length`|1.61622938&middot;10<sup>-35</sup>|*l<sub>P</sub>* - Planck length (m)|
|`planck_mass`|2.17647051&middot;10<sup>-8</sup>|*m<sub>P</sub>* - Planck mass (kg)|
|`planck_temp`|1.41680833e+32|*T<sub>P</sub>* - Planck temperature (K)|
|`planck_time`|5.3911413&middot;10<sup>-44</sup>|*t<sub>P</sub>* - Planck time (s)|
|`red_planck`|1.054571629&middot;10<sup>-34</sup>|*ħ* - Reduced Planck constant (J&middot;s<sup>-1</sup>)|
|`vacuum_imped`|376.730313461770663|*Z<sub>0</sub>* - Impedance of free space (Ω)|
|`vacuum_permea`|1.256637061435917&middot;10<sup>-6</sup>|*μ<sub>0</sub>* - Vacuum permeability (N&middot;A<sup>-2</sup>)|
|`vacuum_permit`|8.854187817620389&middot;10<sup>-12</sup>|*ε<sub>0</sub>* - Vacuum permittivity (F&middot;m<sup>-1</sup>)|
|&nbsp;|**Statistics**|&nbsp;|
|`catalan`|0.915965594177219|*G* - Catalan's constant|
|`glaisher`|1.282427129100623|*A* - Glaisher-Kinkelin constant|
|&nbsp;|**Trigonometry**|&nbsp;|
|`pi`|3.141592653589793|*π* - Perimeter of a circle of diameter 1|
|`tau`|6.283185307179586|*τ* - Double of π|