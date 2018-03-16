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

#### Calling

A function call consists of the function followed by an argument list enclosed in parentheses. The function can be an identifier or any expression returning a function.

    someFunc(arg1, arg2, arg3)

The argument list can be passed as a list object, for example for dynamic calls, using the `*` expanding operator in front of the list object.

    gcd(*[248, 4584]) == gcd(248, 4584)

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

In the following table, a type name followed by a star (*) means that the function accepts a variable argument list of the specified self.

#### Example

The `average` function accepts either List(Number) or Number*. Thus, it can be used either with a list object: `average(myList)` or with varargs: `average(1, 2, 3)`.

| Name | Parameters | Description |
|------|------------|-------------|
{{{funcdoc}}}

Useful (?) constants are also provided, with the maximum supported precision.

| Name | Approximated value | Description |
|------|-------------------:|-------------|
{{{constdoc}}}
