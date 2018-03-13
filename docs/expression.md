# Built-in expression parser

Turing has a built-in mathematical expression parser, which is used when the program is in pseudocode mode.

The language is case-insensitive for keywords, i.e. `FALSE`, `false` and `FaLsE` are the same thing.

## Value types

### Number

Stored using a Python `float`, automatically converted to `int` when needed.

### Boolean

Stored using a Python `bool`, automatically converted to Number when needed (only if strict mode is disabled).

#### Syntax

The following keywords are available:
- `TRUE` / `VRAI` : True value
- `FALSE` / `FAUX` : False value

### String

Stored using a Python `str` (Unicode).

The available operators are:

| Symbol | Operator | Types |
|--------|----------|-------|
| `+` | Plus | Number, String |
| `-` | Minus | Number |
| `*` | Times | Number |
| `/` | Divide | Number |
| `%` | Modulus | Number |
| `^` | Power | Number |
| `<=` | Less than or equal | Number |
| `<` | Strictly less than | Number |
| `>` | Strictly greater than | Number |
| `>=` | Greater than or equal | Number |
| `==` | Equals | All |
| `!=` | Not equals | All |
| `&` / `ET` | Boolean/bitwise AND | Number, Boolean |
| <code>&#124;</code> / `OU` | Boolean/bitwise OR | Number, Boolean |
| `XOR` | Boolean/bitwise XOR | Number, Boolean |

The numbers and booleans are treated the same way as in **plain Python**. In other words, booleans can be treated as numbers (`False` becomes 0 and `True` becomes 1), and numbers can be treated as booleans (0 becomes `False` and everything else becomes `True).

If **strict mode** is enabled, operators can only be used with operands of **identical type**, and **implicit number-boolean casts** are disabled. The `bool` and `num` functions can then be used for that purpose.