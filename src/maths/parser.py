# -*- coding: utf-8 -*-

import re
import types
from typing import List, Tuple, Any

from util import translate
from util.log import Logger
from util.math import proper_str, is_num
from . import nodes


class ValueType:
    """Types of values"""
    STRING, NUMBER, BOOLEAN, LIST, FUNCTION = range(5)

    @staticmethod
    def get_type(obj) -> 'ValueType':
        if type(obj) == list:
            return ValueType.LIST

        if type(obj) == types.FunctionType:
            return ValueType.FUNCTION

        if type(obj) == str:
            return ValueType.STRING

        if type(obj) == bool:
            return ValueType.BOOLEAN

        if is_num(obj):
            return ValueType.NUMBER

        return None

    @staticmethod
    def get_name(type: 'ValueType') -> str:
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

    @staticmethod
    def get_name(type: 'TokenType') -> str:
        for name, value in TokenType.__dict__.items():
            if value == type:
                return name


class Operators:
    """Available operators"""
    math = ["+", "-", "*", "/", "%", "^", "**", "&", "|", "ET", "AND", "OU", "OR",
            "XOR"]  # Mathematical (numeric) operators
    eq = ["==", "!="]  # Basic comparison operators
    rel = ["<=", "<", ">", ">="]  # Relational operators
    comp = eq + rel  # Comparison operators
    boolean = ["ET", "AND", "OU", "OR", "NON", "NOT", "==", "!=", "&", "|", "XOR"]  # Boolean operators
    ops = list(set(math + comp + boolean))  # All operators

    precedence = [
        ["OR", "OU", "|"],
        ["XOR"],
        ["AND", "ET", "&"],
        comp,
        ["+", "-"],
        ["*", "/", "%"],
        ["^", "**"]
    ]

    @staticmethod
    def get_precedence(op: str) -> int:
        return next(i for i, ops in enumerate(Operators.precedence) if op.upper() in ops)

    @staticmethod
    def pretty_print(op: str) -> str:
        return {
            "|": translate("Parser", "OR"),
            "&": translate("Parser", "AND"),
            "NOT": translate("Parser", "NOT")
        }.get(op.upper(), op)


Token = Tuple[TokenType, Any]


class Parser:
    """Main parser class. Transforms a string into an AST tree."""

    expression: str = None
    tokens: List[Token] = None
    index: int = None
    log = None

    def __init__(self, expr: str):
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

    def next_token(self) -> Token:
        """Reads the next token and advances the position."""
        self.index += 1
        return self.tokens[self.index - 1]

    def peek_token(self) -> Token:
        """Reads the next token without affecting position."""
        if not self.can_read():
            return None

        return self.tokens[self.index]

    def match_token(self, token_type: TokenType, value=None) -> bool:
        """Checks if the next token matches the specified token type and (optional) value."""
        return self.can_read() \
               and self.peek_token()[0] == token_type \
               and ((not value)
                    or self.peek_token()[1] in (value
                                                if type(value) == list
                                                else [value]))

    def accept_token(self, token_type: TokenType, value=None) -> bool:
        """If the next token matches, advance and return True, otherwise return False without advancing."""
        if self.match_token(token_type, value):
            self.index += 1
            return True

        return False

    def accept_operator(self, operator: str) -> bool:
        """Wrapper for accept(OPERATOR, operator)."""
        return self.accept_token(TokenType.OPERATOR, operator)

    def expect_token(self, token_type: TokenType, value=None):
        """Asserts the next token is of the specified type and (optional) value. Explodes otherwise."""
        if not self.match_token(token_type, value):
            self.log.error(translate("Parser", "Expected token (%s) '%s'") % (TokenType.get_name(token_type), value))
            return None

        return self.next_token()

    def can_read(self) -> bool:
        """Checks if there is still anything to read."""
        return self.index < len(self.tokens)

    def tokenize(self):
        """Converts the expression string into a linear list of tokens."""
        regex = re.compile(
            r"(\+|-|/|%|\^|\*\*|\*|"
            r"==|!=|<=|<|>|>=|"
            r"\(|\)|\[|\]|{|\}|"
            r"\bET\b|\bAND\b|\bOU\b|\bOR\b|\bXOR\b|\bNON\b|\bNOT\b|"
            r"\bVRAI\b|\bFAUX\b|\bTRUE\b|\bFALSE\b|"
            r"&|\||,| |\"(?:[^\"]*)\")",
            re.IGNORECASE)

        tokenized = [x.strip() for x in regex.split(self.expression) if x.strip()]

        # fix exponents
        new_tokens = []
        idx = 0

        while idx < len(tokenized):
            current = tokenized[idx]

            if idx < len(tokenized) - 2 and current[-1].upper() == "E" and tokenized[idx + 1] in ["+", "-"]:
                # if there is an E followed by a number, this is an exponent notation
                current += tokenized[idx + 1]
                current += tokenized[idx + 2]
                idx += 2

            new_tokens.append(current)
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

    def match_operator(self, expected: List[str]) -> str:
        """Checks if any of the specified operators are to be found."""
        for x in expected:
            if self.accept_operator(x):
                return x

    def parse(self) -> nodes.AstNode:
        """Main parsing routine."""
        self.tokenize()
        return self.parse_expression()

    def parse_expression(self) -> nodes.AstNode:
        """Parses an expression."""
        return self.parse_or()

    def parse_or(self) -> nodes.AstNode:
        """Parses an OR operation."""
        expr = self.parse_xor()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["OR", "OU", "|"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_xor(), "|")
                continue
            break

        return expr

    def parse_xor(self) -> nodes.AstNode:
        """Parses a XOR operation."""
        expr = self.parse_and()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["XOR"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_and(), "XOR")
                continue
            break

        return expr

    def parse_and(self) -> nodes.AstNode:
        """Parses an AND operation."""
        expr = self.parse_equality()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["AND", "ET", "&"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_equality(), "&")
                continue
            break

        return expr

    def parse_equality(self) -> nodes.AstNode:
        """Parses a comparison/equality."""
        expr = self.parse_additive()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(Operators.comp)
            if op:
                expr = nodes.BinOpNode(expr, self.parse_additive(), op)
                continue
            break

        return expr

    def parse_additive(self) -> nodes.AstNode:
        """Parses an addition or subtraction."""
        expr = self.parse_multiplicative()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["+", "-"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_multiplicative(), op)
                continue
            break

        return expr

    def parse_multiplicative(self) -> nodes.AstNode:
        """Parses a product, division, or modulus."""
        expr = self.parse_exponent()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["*", "/", "%"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_exponent(), op)
                continue
            break

        return expr

    def parse_exponent(self) -> nodes.AstNode:
        """Parses an exponentiation."""
        expr = self.parse_unary()

        while self.match_token(TokenType.OPERATOR):
            op = self.match_operator(["^", "**"])
            if op:
                expr = nodes.BinOpNode(expr, self.parse_unary(), op)
                continue
            break

        return expr

    def parse_unary(self) -> nodes.AstNode:
        """Parses an unary operation."""
        op = self.match_operator(["+", "-", "NON", "NOT", "*"])
        if op:
            return nodes.UnaryOpNode(self.parse_unary(), op)

        return self.parse_call_pre()

    def parse_call_pre(self) -> nodes.AstNode:
        """Parses a function call (1)."""
        return self.parse_call(self.parse_term())

    def parse_arg_list(self, array=False) -> List[nodes.AstNode]:
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

        self.expect_token(tok_type, sym_open)

        while not self.match_token(tok_type, sym_end):
            result.append(self.parse_expression())

            if not self.accept_token(TokenType.COMMA):
                break

        self.expect_token(tok_type, sym_end)

        return result

    def parse_param_list(self) -> List[str]:
        """Parses a lambda function parameter list."""
        result = []

        self.expect_token(TokenType.BRACE, "{")

        while not self.match_token(TokenType.BRACE, "}"):
            result.append(self.expect_token(TokenType.IDENTIFIER)[1])

            if not self.accept_token(TokenType.COMMA):
                break

        self.expect_token(TokenType.BRACE, "}")

        return result

    def parse_indexer(self) -> nodes.AstNode:
        """Parses an indexer expression."""
        self.expect_token(TokenType.BRACK, "[")

        expr = self.parse_expression()

        self.expect_token(TokenType.BRACK, "]")

        return expr

    def parse_call(self, left: nodes.AstNode) -> nodes.AstNode:
        """Parses a function call (2)."""
        if self.match_token(TokenType.PAREN, "("):
            return self.parse_call(nodes.CallNode(left, self.parse_arg_list()))
        elif self.match_token(TokenType.BRACK, "["):
            return self.parse_call(nodes.ArrayAccessNode(left, self.parse_indexer()))
        else:
            return left

    def parse_term(self) -> nodes.AstNode:
        """Parses an atomic term."""
        if self.match_token(TokenType.NUMBER):
            return nodes.NumberNode(self.next_token()[1])
        elif self.match_token(TokenType.BOOLEAN):
            return nodes.NumberNode(bool(self.next_token()[1]))
        elif self.match_token(TokenType.STRING):
            return nodes.StringNode(self.next_token()[1])
        elif self.match_token(TokenType.IDENTIFIER):
            return nodes.IdentifierNode(self.next_token()[1])

        elif self.accept_token(TokenType.PAREN, "("):
            stmt = self.parse_expression()
            self.expect_token(TokenType.PAREN, ")")

            return stmt

        elif self.match_token(TokenType.BRACK, "["):
            stmt = nodes.ListNode(self.parse_arg_list(True))

            return stmt

        elif self.match_token(TokenType.BRACE, "{"):
            args = self.parse_param_list()

            self.expect_token(TokenType.PAREN, "(")
            expr = self.parse_expression()
            self.expect_token(TokenType.PAREN, ")")

            return nodes.LambdaNode(args, expr)

        else:
            if not self.can_read():
                self.log.error(translate("Parser", "Unexpected EOL"))
            else:
                self.log.error(
                    translate("Parser", "Unexpected token (%s) '%s'") % (
                        TokenType.get_name(self.peek_token()[0]), self.peek_token()[1]))

            return None

    def beautify(self):
        """Beautifies the expression (adds spaces between operators)."""
        result = ""

        prev2: Token = None
        prev1: Token = None

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

def quick_parse(expr: str):
    p = Parser(expr)
    return p.parse()