# -*- coding: utf-8 -*-

import maths.nodes as nodes
from util.log import Logger
from util.math import proper_str, is_num
import types
import re
import util

translate = util.translate


class ValueType:
    """Types of values"""
    STRING, NUMBER, BOOLEAN, LIST, FUNCTION = range(5)

    def getType(self):
        if type(self) == list:
            return ValueType.LIST

        if type(self) == types.FunctionType:
            return ValueType.FUNCTION

        if type(self) == str:
            return ValueType.STRING

        if type(self) == bool:
            return ValueType.BOOLEAN

        if is_num(self):
            return ValueType.NUMBER

        return None

    def getName(type):
        for name, value in ValueType.__dict__.items():
            if value == type:
                return name


class TokenType:
    """Token types used during the lexing process"""
    OPERATOR, STRING, NUMBER, BOOLEAN, IDENTIFIER, COMMA, PAREN, BRACK, BRACE = range(9)

    Term = [NUMBER, BOOLEAN, IDENTIFIER, STRING]
    UnaryVal = ["+", "-", "*"]
    Opening = ["(", "[", "{"]
    Closing = [")", "]", "}"]
    TrueVal = ["TRUE", "VRAI"]
    FalseVal = ["FALSE", "FAUX"]
    Block = [PAREN, BRACK, BRACE]

    def getName(self):
        for name, value in TokenType.__dict__.items():
            if value == self:
                return name


class Operators:
    """Available operators"""
    math = ["+", "-", "*", "/", "%", "^", "&", "|", "ET", "AND", "OU", "OR", "XOR"]  # Mathematical (numeric) operators
    eq = ["==", "!="]  # Basic comparison operators
    rel = ["<=", "<", ">", ">="]  # Relational operators
    comp = eq + rel  # Comparison operators
    boolean = ["ET", "AND", "OU", "OR", "NON", "NOT", "==", "!=", "&", "|", "XOR"]  # Boolean operators
    ops = list(set(math + comp + boolean))  # All operators


class Parser:
    """Main parser class. Transforms a string into an AST tree."""

    expression = None
    tokens = None
    index = None
    log = None

    def __init__(self, expr):
        """Initializes the Parser instance.

        expr -- the expression to be parsed"""
        self.expression = expr
        self.tokens = []
        self.index = 0
        self.log = Logger("Parser")
        self.fix_mul()

    def fix_mul(self):
        """Fixes the multiplication syntax by adding starts (*) between numbers and identifiers.

        Example: 2pi becomes 2*pi"""
        for i in range(1, len(self.expression)):
            if self.expression[i - 1].isdigit() and self.expression[i].isalpha():
                if i < len(self.expression) - 1:
                    if self.expression[i].upper() == "E":
                        if self.expression[i - 1].isdigit() or self.expression[i - 1] in ["+", "-"]:
                            continue

                self.expression = self.expression[:i] + "*" + self.expression[i:]

    def fix_mul_tok(self):
        """More advanced version of fix_mul, works at token level."""
        result = []

        previous = (None, None)

        for tok in self.tokens:
            if previous[0] == TokenType.NUMBER and tok[0] == TokenType.IDENTIFIER:
                result.append((TokenType.OPERATOR, "*"))

            result.append(tok)

            previous = tok

        self.tokens = result

    def nextToken(self):
        """Reads the next token and advances the position."""
        self.index += 1
        return self.tokens[self.index - 1]

    def peekToken(self):
        """Reads the next token without affecting position."""
        if not self.canRead():
            return None

        return self.tokens[self.index]

    def matchToken(self, tokType, value=None):
        """Checks if the next token matches the specified token type and (optional) value."""
        return self.canRead() \
               and self.peekToken()[0] == tokType \
               and ((not value)
                    or self.peekToken()[1] in (value
                                               if type(value) == list
                                               else [value]))

    def acceptToken(self, tokType, value=None):
        """If the next token matches, advance and return True, otherwise return False without advancing."""
        if self.matchToken(tokType, value):
            self.index += 1
            return True

        return False

    def acceptOperator(self, opType):
        """Wrapper for accept(OPERATOR, opType)."""
        return self.acceptToken(TokenType.OPERATOR, opType)

    def expectToken(self, opType, value=None):
        """Asserts the next token is of the specified type and (optional) value. Explodes otherwise."""
        if not self.matchToken(opType, value):
            self.log.error(translate("Parser", "Expected token (%s) '%s'") % (TokenType.getName(opType), value))
            return None

        return self.nextToken()

    def canRead(self):
        """Checks if there is still anything to read."""
        return self.index < len(self.tokens)

    def tokenize(self):
        """Converts the expression string into a linear list of tokens."""
        regex = re.compile(
            r"(\+|-|\*|/|%|\^|==|!=|<=|<|>|>=|\(|\)|\[|\]|{|\}|\bET\b|\bAND\b|\bOU\b|\bOR\b|\bXOR\b|\bNON\b|\bNOT\b|\bVRAI\b|\bFAUX\b|\bTRUE\b|\bFALSE\b|&|\||,| )",
            re.IGNORECASE)

        tok = [x.strip() for x in regex.split(self.expression) if x.strip()]

        # fix exponents
        new_tokens = []
        idx = 0

        while idx < len(tok):
            cur = tok[idx]

            if idx < len(tok) - 2 and cur[-1].upper() == "E" and tok[idx + 1] in ["+", "-"]:
                # if there is an E followed by a number, this is an exponent notation
                cur += tok[idx + 1]
                cur += tok[idx + 2]
                idx += 2

            new_tokens.append(cur)
            idx += 1

        for token in new_tokens:
            if token.upper() in Operators.ops:
                self.tokens.append((TokenType.OPERATOR, token.upper()))
            elif token.upper() in TokenType.TrueVal:
                self.tokens.append((TokenType.BOOLEAN, True))
            elif token.upper() in TokenType.FalseVal:
                self.tokens.append((TokenType.BOOLEAN, False))
            elif token == ",":
                self.tokens.append((TokenType.COMMA, ","))
            elif token in ["(", ")"]:
                self.tokens.append((TokenType.PAREN, token))
            elif token in ["[", "]"]:
                self.tokens.append((TokenType.BRACK, token))
            elif token in ["{", "}"]:
                self.tokens.append((TokenType.BRACE, token))
            else:
                if token[0] == token[-1] == '"':
                    self.tokens.append((TokenType.STRING, token[1:-1]))
                else:
                    try:
                        if re.search('^[0-9]+$', token):
                            num = int(token)
                        else:
                            num = float(token)
                        self.tokens.append((TokenType.NUMBER, num))
                    except:
                        if re.search('^[a-zA-Z_0-9]+$', token):
                            self.tokens.append((TokenType.IDENTIFIER, token))
                        else:
                            self.tokens.append((None, token))

        self.fix_mul_tok()

    def matchOperator(self, expected):
        """Checks if any of the specified operators are to be found."""
        for x in expected:
            if self.acceptOperator(x):
                return x

    def parse(self):
        """Main parsing routine."""
        self.tokenize()
        return self.parseExpr()

    def parseExpr(self):
        """Parses an expression."""
        return self.parseOr()

    def parseOr(self):
        """Parses an OR operation."""
        expr = self.parseXor()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["OR", "OU", "|"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseXor(), "|")
                continue
            break

        return expr

    def parseXor(self):
        """Parses a XOR operation."""
        expr = self.parseAnd()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["XOR"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseAnd(), "XOR")
                continue
            break

        return expr

    def parseAnd(self):
        """Parses an AND operation."""
        expr = self.parseEquality()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["AND", "ET", "&"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseEquality(), "&")
                continue
            break

        return expr

    def parseEquality(self):
        """Parses a comparison/equality."""
        expr = self.parseAdditive()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(Operators.comp)
            if op:
                expr = nodes.BinOpNode(expr, self.parseAdditive(), op)
                continue
            break

        return expr

    def parseAdditive(self):
        """Parses an addition or subtraction."""
        expr = self.parseMultiplicative()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["+", "-"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseMultiplicative(), op)
                continue
            break

        return expr

    def parseMultiplicative(self):
        """Parses a product, division, or modulus."""
        expr = self.parseExponent()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["*", "/", "%"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseExponent(), op)
                continue
            break

        return expr

    def parseExponent(self):
        """Parses an exponentiation."""
        expr = self.parseUnary()

        while self.matchToken(TokenType.OPERATOR):
            op = self.matchOperator(["^"])
            if op:
                expr = nodes.BinOpNode(expr, self.parseUnary(), op)
                continue
            break

        return expr

    def parseUnary(self):
        """Parses an unary operation."""
        op = self.matchOperator(["+", "-", "NON", "NOT", "*"])
        if op:
            return nodes.UnaryOpNode(self.parseUnary(), op)

        return self.parseCallPre()

    def parseCallPre(self):
        """Parses a function call (1)."""
        return self.parseCall(self.parseTerm())

    def parseArgList(self, array=False):
        """Parses an argument list."""
        result = []

        if array:
            tok_type = TokenType.BRACK
            sym_open = "["
            sym_end = "]"
        else:
            tok_type = TokenType.PAREN
            sym_open = "("
            sym_end = ")"

        self.expectToken(tok_type, sym_open)

        while not self.matchToken(tok_type, sym_end):
            result.append(self.parseExpr())

            if not self.acceptToken(TokenType.COMMA):
                break

        self.expectToken(tok_type, sym_end)

        return result

    def parseParamList(self):
        """Parses a lambda function parameter list."""
        result = []

        self.expectToken(TokenType.BRACE, "{")

        while not self.matchToken(TokenType.BRACE, "}"):
            result.append(self.expectToken(TokenType.IDENTIFIER)[1])

            if not self.acceptToken(TokenType.COMMA):
                break

        self.expectToken(TokenType.BRACE, "}")

        return result

    def parseIndexer(self):
        """Parses an indexer expression."""
        self.expectToken(TokenType.BRACK, "[")

        expr = self.parseExpr()

        self.expectToken(TokenType.BRACK, "]")

        return expr

    def parseCall(self, left):
        """Parses a function call (2)."""
        if self.matchToken(TokenType.PAREN, "("):
            return self.parseCall(nodes.CallNode(left, self.parseArgList()))
        elif self.matchToken(TokenType.BRACK, "["):
            return self.parseCall(nodes.ArrayAccessNode(left, self.parseIndexer()))
        else:
            return left

    def parseTerm(self):
        """Parses an atomic term."""
        if self.matchToken(TokenType.NUMBER):
            return nodes.NumberNode(float(self.nextToken()[1]))
        elif self.matchToken(TokenType.BOOLEAN):
            return nodes.NumberNode(bool(self.nextToken()[1]))
        elif self.matchToken(TokenType.STRING):
            return nodes.StringNode(self.nextToken()[1])
        elif self.matchToken(TokenType.IDENTIFIER):
            return nodes.IdentifierNode(self.nextToken()[1])

        elif self.acceptToken(TokenType.PAREN, "("):
            stmt = self.parseExpr()
            self.expectToken(TokenType.PAREN, ")")

            return stmt

        elif self.matchToken(TokenType.BRACK, "["):
            stmt = nodes.ListNode(self.parseArgList(True))

            return stmt

        elif self.matchToken(TokenType.BRACE, "{"):
            args = self.parseParamList()

            self.expectToken(TokenType.PAREN, "(")
            expr = self.parseExpr()
            self.expectToken(TokenType.PAREN, ")")

            return nodes.LambdaNode(args, expr)

        else:
            if not self.canRead():
                self.log.error(translate("Parser", "Unexpected EOL"))
            else:
                self.log.error(
                    translate("Parser", "Unexpected token (%s) '%s'") % (
                    TokenType.getName(self.peekToken()[0]), self.peekToken()[1]))

            return None

    def beautify(self):
        """Beautifies the expression (adds spaces between operators)."""
        result = ""

        prev2 = None
        prev1 = None

        for typ, val in self.tokens:
            # remove space between operator and term only if operator is unary
            if (result  # only if string contains contents
                    and result[-1] == " "  # only if there is a space to remove
                    and (typ in TokenType.Term or val in TokenType.Opening)  # only if this is a term or block
                    and ((prev1[1] in TokenType.UnaryVal)  # only for unary op
                         and ((not prev2)
                              or (prev2[
                                      1] in TokenType.Opening + TokenType.UnaryVal)  # no space between opening and unary op
                              or (prev2[0] == TokenType.COMMA)  # no space before comma
                         )
                    )
            ):
                result = result[:-1]

            # add space before operator only if after term or closing
            if (typ == TokenType.OPERATOR  # only if operator
                    and prev1  # and something before
                    and (prev1[1] not in TokenType.Opening)  # no space after opening
                    and (prev1[0] != TokenType.OPERATOR
                         or (prev2
                             and prev2[1] not in TokenType.Opening
                         )
                    )
            ):
                result += " "

            # remove space for i
            if typ == TokenType.IDENTIFIER and val == "i":
                if prev1 and prev1 == (TokenType.OPERATOR, "*"):
                    result = result[:-3]

            # token
            if typ in [TokenType.NUMBER, TokenType.BOOLEAN]:
                result += proper_str(val)
            elif typ == TokenType.STRING:
                result += '"' + str(val) + '"'
            else:
                result += str(val)

            # comma is always followed by space
            if typ == TokenType.COMMA:
                result += " "

            if (typ == TokenType.OPERATOR
                    and prev1
                    and prev1[0] != TokenType.OPERATOR
                    and prev1[1] not in TokenType.Opening):
                result += " "

            prev2 = prev1
            prev1 = (typ, val)

        # remove double whitespaces
        return re.sub("\s\s+", " ", result)
