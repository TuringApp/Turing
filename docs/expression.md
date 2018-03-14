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

| Name | Parameters | Description |
|------|------------|-------------|
|&nbsp;|**Basic**|&nbsp;|
|`round` / `arrondi`|<ul><li>`num` (Number)</li><li>`prec` (Integer)</li></ul>|Rounds `num` to the nearest integer / (if specified) to `prec` decimals.|
|`abs`|<ul><li>`num` (Number)</li></ul>|Returns the absolute value of `num`.|
|`abs` / `rac`|<ul><li>`num` (Number) >= 0</li></ul>|Returns the square root of `num`.|
|`root`|<ul><li>`num` (Number)</li><li>`n` (Number) != 0</li></ul>|Returns the `n`-th root of `num`.|
|`pow` / `puiss`|<ul><li>`num` (Number)</li><li>`p` (Number)</li></ul>|Returns `num` to the `p`-th power.|
|`exp`|<ul><li>`num` (Number)</li></ul>|Returns *e* to the power of `num`.|
|`ln`|<ul><li>`num` (Number)</li></ul>|Returns the natural (base-*e*) logarithm of `num`.|
|`log`|<ul><li>`num` (Number)</li><li>`b` (Number) != 0, default = 10</li></ul>|Returns the base-`b` logarithm of `num`.|
|`log10`|<ul><li>`num` (Number)</li></ul>|Returns the base-10 logarithm of `num`.|
|`floor`|<ul><li>`num` (Number)</li></ul>|Returns the largest integer less than or equal to `num`.|
|`ceil`|<ul><li>`num` (Number)</li></ul>|Returns the smallest integer greater than or equal to `num`.|
|`sign`|<ul><li>`num` (Number)</li></ul>|Returns the sign of `num` (-1 if negative, 1 if positive, 0 otherwise).|
|`gcd`|<ul><li>`a` (Integer)</li><li>`b` (Integer)</li></ul>|Returns the greatest common divisor of `a` and `b`.|
|&nbsp;|**Type conversion**|&nbsp;|
|&nbsp;|**Basic**|&nbsp;|
|`round` / `arrondi`|<ul><li>`num` (Number)</li><li>`prec` (Integer)</li></ul>|Rounds `num` to the nearest integer / (if specified) to `prec` decimals.|
|`abs`|<ul><li>`num` (Number)</li></ul>|Returns the absolute value of `num`.|
|`sqrt` / `rac`|<ul><li>`num` (Number) >= 0</li></ul>|Returns the square root of `num`.|
|`root`|<ul><li>`num` (Number)</li><li>`n` (Number) != 0</li></ul>|Returns the `n`-th root of `num`.|
|`pow` / `puiss`|<ul><li>`num` (Number)</li><li>`p` (Number)</li></ul>|Returns `num` to the `p`-th power.|
|`exp`|<ul><li>`num` (Number)</li></ul>|Returns *e* to the power of `num`.|
|`ln`|<ul><li>`num` (Number)</li></ul>|Returns the natural (base *e*) logarithm of `num`.|
|`log`|<ul><li>`num` (Number)</li></li>`b` (Number) default: 10</li></ul>|Returns the base-`b` logarithm of `num`.|
|`log10`|<ul><li>`num` (Number)</li></ul>|Returns the base-10 logarithm of `num`.|
|`floor`|<ul><li>`num` (Number)</li></ul>|Returns the largest integer less than or equal to `num`.|
|`ceil`|<ul><li>`num` (Number)</li></ul>|Returns the smallest integer greater than or equal to `num`.|
|`sign`|<ul><li>`num` (Number)</li></ul>|Returns the sign of `num` (-1 if negative, 1 if positive, 0 otherwise).|
|`gcd`|<ul><li>`a` (Integer)</li><li>`b` (Integer)</li></ul>|Returns the greatest common divisor of `a` and `b`.|
|&nbsp;|**Type conversion**|&nbsp;|
|`c_bool`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to Boolean.|
|`c_num`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to Number.|
|`c_list`|<ul><li>`obj` (Any)</li></ul>|Tries to convert `obj` to List.|
|`c_str`|<ul><li>`obj` (Any)</li></ul>|Converts `obj` to String.|
|&nbsp;|**Geometry**|&nbsp;|
|&nbsp;|**Statistics**|&nbsp;|
|&nbsp;|**Trigonometry**|&nbsp;|

Useful (?) constants are also provided, with the maximum supported precision.

| Name | Approximated value | Description |
|------|-------------------:|-------------|
|`pi`|3.141592653589793|π, perimeter of a circle with diameter 1.|
|`e`|2.718281828459045|Euler number|
|`tau`|6.283185307179586|τ = 2⋅π|
|`phi`|1.618033988749894|φ - The golden ratio|
|`euler_gamma`|0.577215664901532|γ - Euler-Mascheroni constant|
|`catalan`|0.915965594177219|*G* - Catalan's constant|
|`glaisher`|1.282427129100622|*A* - Glaisher-Kinkelin constant|
|`khinchin`|2.685452001065306|*K<sub>0</sub>* - Khinchin-s constant|
|`celerity`|299792458|*c* - Speed of light in vacuum (m.s<sup>-1</sup>)|
|`planck`|6.62607004081⋅10<sup>-34</sup>|*h* - Planck constant (J⋅s<sup>-1</sup>)|
|`red_planck`|1.054571629⋅10<sup>-34</sup>|*ħ* - Reduced Planck constant (J⋅s<sup>-1</sup>)|
|`planck_time`|5.3911413⋅10<sup>-44</sup>|*t<sub>P</sub>* - Planck time (s)|
|`planck_temp`|1.41680833⋅10<sup>32</sup>|*T<sub>P</sub>* - Planck temperature (K)|
|`planck_mass`|2.17647051⋅10<sup>-8</sup>|*m<sub>P</sub>* - Planck mass (kg)|
|`planck_length`|1.61622938⋅10<sup>-35</sup>|*l<sub>P</sub>* - Planck length (m)|
|`planck_charge`|1.8755459⋅10<sup>-18</sup>|*q<sub>P</sub>* - Planck charge (C)|
|`gravity`|6.6740831⋅10<sup>-11</sup>|*G* - Gravitational constant (N⋅m<sup>2</sup>⋅kg<sup>-2</sup>)|
|`vacuum_permit`|8.854187817620389⋅10<sup>-12</sup>|*ε<sub>0</sub>* - Vacuum permittivity (F⋅m<sup>-1</sup>)|
|`vacuum_permea`|1.256637061435917⋅10<sup>-6</sup>|*μ<sub>0</sub>* - Vacuum permeability (N⋅A<sup>-2</sup>)|
|`vacuum_imped`|376.730313461770655|*Z<sub>0</sub>* - Impedance of free space (Ω)|
|`inf`|+∞|∞ - Positive infinity|