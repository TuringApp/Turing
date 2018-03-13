# -*- coding: utf-8 -*-

import maths.nodes as nodes
from util.log import Logger
from util.math import properstr

class TokenType:
	"""Token types used during the lexing process"""
	OPERATOR, STRING, NUMBER, IDENTIFIER, COMMA, PAREN, BRACK, BRACE = range(8)

	Term = [NUMBER, IDENTIFIER, STRING]
	InBetween = [OPERATOR, COMMA]
	SpaceAfter = [COMMA, PAREN, BRACK, BRACE]
	SpaceBefore = Term + InBetween
	UnaryVal = ["+", "-"]
	Opening = ["(", "[", "{"]
	Closing = [")", "]", "}"]

	def getName(type):
		for n, v in TokenType.__dict__.items():
			if v == type:
				return n

class Operators:
	"""Availaboe operators"""
	math = ["+", "-", "*", "/", "%", "^", "&", "|", "XOR"]       # Mathematical (numeric) operators
	comp = ["==", "!=", "<=", "<", ">", ">="]                    # Relational (comparison) operators
	boolean = ["ET", "OU", "NON"]                                # Boolean operators
	ops = math + comp + boolean                                  # All operators

class Parser:
	"""Main parser class. Transforms a string into an AST tree."""

	expression = None
	tokens = None
	idx = None
	log = None

	def __init__(self, expr):
		"""Initializes the Parser instance.

		expr -- the expression to be parsed"""
		self.expression = expr
		self.tokens = []
		self.idx = 0
		self.log = Logger("Parser")
		self.fix_mul()

	def fix_mul(self):
		"""Fixes the multiplication syntax by adding starts (*) between numbers and identifies.

		Example: 2pi becomes 2*pi"""
		for i in range(1, len(self.expression)):
			if self.expression[i - 1].isdigit() and self.expression[i].isalpha():
				self.expression = self.expression[:i] + "*" + self.expression[i:]

	def fix_mul_tok(self):
		res = []

		ptok = (None, None)

		for tok in self.tokens:
			if ptok[0] == TokenType.NUMBER and tok[0] == TokenType.IDENTIFIER:
				res.append((TokenType.OPERATOR, "*"))

			res.append(tok)

			ptok = tok

		self.tokens = res

	def nextToken(self):
		"""Reads the next token and advances the position."""
		self.idx += 1
		return self.tokens[self.idx - 1]

	def peekToken(self):
		"""Reads the next token without affecting position."""
		if not self.canRead():
			return None

		return self.tokens[self.idx]

	def match(self, tokType, value=None):
		"""Checks if the next token matches the specified token type and (optional) value."""
		return self.canRead() and self.peekToken()[0] == tokType and ((not value) or self.peekToken()[1] in (value if type(value) == list else [value]))

	def accept(self, tokType, value=None):
		"""If the next token matches, advance and return True, otherwise return False without advancing."""
		if self.match(tokType, value):
			self.idx += 1
			return True

		return False

	def acceptOp(self, opType):
		"""Wrapper for accept(OPERATOR, opType)."""
		return self.accept(TokenType.OPERATOR, opType)

	def expect(self, opType, value=None):
		"""Asserts the next token is of the specified type and (optional) value. Explodes otherwise."""
		if not self.match(opType, value):
			self.log.error("Expected token (%s) '%s'" % (TokenType.getName(opType), value))
			return None

		return self.nextToken()

	def canRead(self):
		"""Checks if there is still anything to read."""
		return self.idx < len(self.tokens)

	def tokenize(self):
		"""Converts the expression string into a linear list of tokens."""
		import re
		regex = re.compile(r'(\+|-|\*|/|%|\^|==|!=|<=|<|>|>=|\(|\)|\[|\]|\{|\}|\bET\b|\bOU\b|\bXOR\b|\bNON\b|&|\||,| )', re.IGNORECASE)
		tok = [x.strip() for x in regex.split(self.expression) if x.strip()]

		for token in tok:
			if token.upper() in Operators.ops:
				self.tokens.append((TokenType.OPERATOR, token.upper()))
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
						num = float(token)
						self.tokens.append((TokenType.NUMBER, num))
					except:
						if re.search('^[a-zA-Z_0-9]+$', token):
							self.tokens.append((TokenType.IDENTIFIER, token))
						else:
							self.tokens.append((None, token))

		self.fix_mul_tok()

	def peekOp(self, expected):
		"""Checks if any of the specified operators are to be found."""
		for x in expected:
			if self.acceptOp(x):
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

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["OU", "|"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseXor(), "|")
				continue
			break

		return expr

	def parseXor(self):
		"""Parses a XOR operation."""
		expr = self.parseAnd()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["XOR"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseAnd(), "XOR")
				continue
			break

		return expr

	def parseAnd(self):
		"""Parses an AND operation."""
		expr = self.parseEquality()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["ET", "&"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseEquality(), "&")
				continue
			break

		return expr

	def parseEquality(self):
		"""Parses a comparison/equality."""
		expr = self.parseAdditive()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(Operators.comp)
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseAdditive(), op)
				continue
			break

		return expr

	def parseAdditive(self):
		"""Parses an addition or subtraction."""
		expr = self.parseMultiplicative()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["+", "-"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseMultiplicative(), op)
				continue
			break

		return expr

	def parseMultiplicative(self):
		"""Parses a product, division, exponentiation or modulus."""
		expr = self.parseUnary()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["^", "*", "/", "%"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = nodes.BinOpNode(expr, self.parseUnary(), op)
				continue
			break

		return expr

	def parseUnary(self):
		"""Parses an unary operation."""
		op = self.peekOp(["-", "NON"])
		if op:
			self.accept(TokenType.OPERATOR)
			return nodes.UnaryOpNode(self.parseUnary(), op)

		return self.parseCallPre()

	def parseCallPre(self):
		"""Parses a function call (1)."""
		return self.parseCall(self.parseTerm())

	def parseArgList(self, array = False):
		"""Parses an argument list."""
		ret = []

		if array:
			ttype = TokenType.BRACK
			topen = "["
			tend = "]"
		else:
			ttype = TokenType.PAREN
			topen = "("
			tend = ")"

		self.expect(ttype, topen)

		while not self.match(ttype, tend):
			ret.append(self.parseExpr())
			if not self.accept(TokenType.COMMA):
				break

		self.expect(ttype, tend)

		return ret

	def parseParamList(self):
		"""Parses a lambda function parameter list."""
		ret = []

		self.expect(TokenType.BRACE, "{")

		while not self.match(TokenType.BRACE, "}"):
			ret.append(self.expect(TokenType.IDENTIFIER)[1])
			if not self.accept(TokenType.COMMA):
				break

		self.expect(TokenType.BRACE, "}")

		return ret

	def parseIndexer(self):
		"""Parses an indexer expression."""
		self.expect(TokenType.BRACK, "[")

		expr = self.parseExpr()

		self.expect(TokenType.BRACK, "]")

		return expr

	def parseCall(self, left):
		"""Parses a function call (2)."""
		if self.match(TokenType.PAREN, "("):
			return self.parseCall(nodes.CallNode(left, self.parseArgList()))
		elif self.match(TokenType.BRACK, "["):
			return self.parseCall(nodes.ArrayAccessNode(left, self.parseIndexer()))
		else:
			return left

	def parseTerm(self):
		"""Parses an atomic term."""
		if self.match(TokenType.NUMBER):
			return nodes.NumberNode(float(self.nextToken()[1]))
		elif self.accept(TokenType.PAREN, "("):
			stmt = self.parseExpr()
			self.expect(TokenType.PAREN, ")")
			return stmt
		elif self.match(TokenType.BRACK, "["):
			stmt = nodes.ListNode(self.parseArgList(True))
			return stmt
		elif self.match(TokenType.BRACE, "{"):
			args = self.parseParamList()
			self.expect(TokenType.PAREN, "(")
			expr = self.parseExpr()
			self.expect(TokenType.PAREN, ")")
			return nodes.LambdaNode(args, expr)
		elif self.match(TokenType.STRING):
			return nodes.StringNode(self.nextToken()[1])
		elif self.match(TokenType.IDENTIFIER):
			return nodes.IdentifierNode(self.nextToken()[1])
		else:
			if not self.canRead():
				self.log.error("Unexpected EOL")
			else:
				self.log.error("Unexpected token (%s) '%s'" % (TokenType.getName(self.peekToken()[0]), self.peekToken()[1]))
			return None

	def beautify(self):
		"""Beautifies the expression (adds spaces between operators)."""
		ret = ""

		prev2 = None
		prev1 = None

		for typ, val in self.tokens:
			if typ in TokenType.Term and (prev1 and (prev1[1] in TokenType.UnaryVal) and ((not prev2) or (prev2[1] in TokenType.Opening))):
				ret = ret[:-1]

			if typ == TokenType.OPERATOR and ((not prev1) or (prev1[1] not in TokenType.Opening)):
				ret += " "

			if typ == TokenType.NUMBER:
				ret += properstr(val)
			else:
				ret += str(val)

			if typ == TokenType.COMMA:
				ret += " "

			if typ == TokenType.OPERATOR:
				ret += " "

			prev2 = prev1
			prev1 = (typ, val)

		return ret.strip()

	def beautify2(self):
		"""Beautifies the expression (adds spaces between operators)."""
		ret = ""

		prev2 = None
		prev1 = None

		for typ, val in self.tokens:		
			if ret and typ in TokenType.SpaceAfter and typ and ret[-1] == " " and ((not prev1) or (prev1[0] in TokenType.SpaceBefore)):
				ret = ret[:-1]

			if ret and typ in [TokenType.OPERATOR] and val not in TokenType.UnaryVal and ret[:-1] != " " and (prev1 and (prev1[0] in TokenType.SpaceAfter)):
				ret += " "

			if typ == TokenType.NUMBER:
				ret += properstr(val)
			else:
				ret += str(val)

			if typ in TokenType.SpaceBefore + [TokenType.COMMA]:
				ret += " "	

			prev2 = prev1
			prev1 = (typ, val)

		return ret.strip()