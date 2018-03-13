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