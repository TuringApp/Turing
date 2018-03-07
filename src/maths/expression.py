# -*- coding: utf-8 -*-

class TokenType:
	OPERATOR, STRING, NUMBER, IDENTIFIER, COMMA, PAREN = range(6)

class Operators:
	math = ["+", "-", "*", "/", "%", "^"]
	comp = ["==", "!=", "<=", "<", ">", ">="]
	boolean = ["ET", "OU", "XOR", "NON"]
	ops = math + comp + boolean

class AstNode:
	def __init__(self):
		pass

class OPERATORNode(AstNode):
	left = None
	right = None
	opType = None

	def __init__(self, left, right, opType):
		self.left = left
		self.right = right
		self.opType = opType

class UnaryOpNode(AstNode):
	value = None
	opType = None

	def __init__(self, value, opType):
		self.value = value
		self.opType = opType

class CallNode(AstNode):
	func = None
	args = None

	def __init__(self, func, args):
		self.func = func
		self.args = args

class NumberNode(AstNode):
	value = None

	def __init__(self, value):
		self.value = value

class StringNode(AstNode):
	value = None

	def __init__(self, value):
		self.value = value

class IdentifierNode(AstNode):
	value = None

	def __init__(self, value):
		self.value = value

class Parser:
	expression = None
	tokens = None
	idx = None

	def __init__(self, expr):
		self.expression = expr
		self.tokens = []
		self.idx = 0
		self.fix_mul()

	def fix_mul(self):
		for i in range(1, len(self.expression)):
			if self.expression[i - 1].isdigit() and self.expression[i].isalpha():
				self.expression = self.expression[:i] + "*" + self.expression[i:]

	def error(msg, dat=None):
		print("parser: " + msg)

	def nextToken(self):
		self.idx += 1
		return self.tokens[self.idx - 1]

	def peekToken(self):
		return self.tokens[self.idx]

	def match(self, opType, value=None):
		return self.canRead() and self.peekToken()[0] == opType and ((not value) or self.peekToken()[1] in (value if type(value) == list else [value]))

	def accept(self, opType, value=None):
		if self.match(opType, value):
			self.idx += 1
			return True

		return False

	def acceptOp(self, opType):
		return self.accept(TokenType.OPERATOR, opType)

	def expect(self, opType, value=None):
		if not self.match(opType, value):
			print("'%s' attendu" % value)
			return None

		return self.nextToken()

	def canRead(self):
		return self.idx < len(self.tokens)

	def tokenize(self):
		import re
		regex = re.compile(r'(\+|-|\*|/|%|\^|==|!=|<=|<|>|>=|\(|\)|\bET\b|\bOU\b|\bXOR\b|\bNON\b|,)')
		tok = [x.strip() for x in regex.split(self.expression) if x.strip()]

		for token in tok:
			if token.upper() in Operators.ops:
				self.tokens.append((TokenType.OPERATOR, token.upper()))
			elif token == ",":
				self.tokens.append((TokenType.COMMA, ","))
			elif token in ["(", ")"]:
				self.tokens.append((TokenType.PAREN, token))
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

	def peekOp(self, expected):
		for x in expected:
			if self.acceptOp(x):
				return x

	def parse(self):
		self.tokenize()
		return self.parseExpr()

	def parseExpr(self):
		return self.parseEquality()

	def parseEquality(self):
		expr = self.parseAdditive()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(Operators.comp)
			if op:
				self.accept(TokenType.OPERATOR)
				expr = OPERATORNode(expr, self.parseAdditive(), op)
				continue
			break

		return expr

	def parseAdditive(self):
		expr = self.parseMultiplicative()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["+", "-"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = OPERATORNode(expr, self.parseMultiplicative(), op)
				continue
			break

		return expr

	def parseMultiplicative(self):
		expr = self.parseUnary()

		while self.match(TokenType.OPERATOR):
			op = self.peekOp(["^", "*", "/", "%"])
			if op:
				self.accept(TokenType.OPERATOR)
				expr = OPERATORNode(expr, self.parseUnary(), op)
				continue
			break

		return expr

	def parseUnary(self):
		op = self.peekOp(["-", "NON"])
		if op:
			self.accept(TokenType.OPERATOR)
			return UnaryOpNode(self.parseUnary(), op)

		return self.parseCallPre()

	def parseCallPre(self):
		return self.parseCall(self.parseTerm())

	def parseArgList(self):
		ret = []

		self.expect(TokenType.PAREN, "(")

		while not self.match(TokenType.PAREN, ")"):
			ret.append(self.parseExpr())
			if not self.accept(TokenType.COMMA):
				break

		self.expect(TokenType.PAREN, ")")

		return ret

	def parseCall(self, left):
		if type(left) == IdentifierNode and self.match(TokenType.PAREN, "("):
			return CallNode(left.value, self.parseArgList())
		else:
			return left

	def parseTerm(self):
		if self.match(TokenType.NUMBER):
			return NumberNode(float(self.nextToken()[1]))
		elif self.accept(TokenType.PAREN, "("):
			stmt = self.parseExpr()
			self.expect(TokenType.PAREN, ")")
			return stmt
		elif self.match(TokenType.STRING):
			return StringNode(self.nextToken()[1])
		elif self.match(TokenType.IDENTIFIER):
			return IdentifierNode(self.nextToken()[1])
		else:
			error("pk tu fais ça")
			return None