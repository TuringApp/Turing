# Built-in expression parser

Turing has a built-in mathematical expression parser, which is used when the program is in pseudocode mode.

There are three value types :
- Number
- Boolean
- String

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

If **strict mode** is enabled, operators can only be used with operands of **identical type**, and **implicit number-boolean casts** are disabled. The `bool` and `int` functions can then be used for that purpose.