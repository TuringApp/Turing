class TokenType:
	BINOP, STRING, NUMBER, IDENTIFIER, COMMA, PAREN = range(6)

class Operators:
	math = ["+", "-", "*", "/", "%", "̂^"]
	comp = ["==", "!=", "<=", "<", ">", ">="]
	boolean = ["ET", "OU", "XOR", "NON"]
	ops = math + comp + boolean

class AstNode:
	def __init__(self):
		pass

class BinOpNode(AstNode):
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
		return self.accept(TokenType.BINOP, opType)

	def expect(self, opType, value=None):
		if not self.match(opType, value):
			error("Erreur")
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
				self.tokens.append((TokenType.BINOP, token.upper()))
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
		left = self.parseAdditive()

		op = self.peekOp(Operators.comp)

		if op:
			right = self.parseEquality()
			return BinOpNode(left, right, op)

		return left

	def parseAdditive(self):
		expr = parseMultiplicative()

		while match(TokenType.BINOP):
			op = self.peekOp(["+", "-"])
			if op:
				accept(TokenType.BINOP)
				expr = BinOpNode(expr, parseMultiplicative(), op)
				continue
			break

		left = self.parseMultiplicative()

		op = self.peekOp(["+", "-"])

		if op:
			right = self.parseAdditive()
			return BinOpNode(left, right, op)

		return left

	def parseMultiplicative(self):
		left = self.parseUnary()

		op = self.peekOp(["*", "/", "%"])

		if op:
			right = self.parseMultiplicative()
			return BinOpNode(left, right, op)

		return left

	def parseUnary(self):
		if self.acceptOp("-"):
			return UnaryOpNode(self.parseUnary(), "-")
		else:
			return self.parseCallPre()

	def parseCallPre(self):
		return self.parseCall(self.parseTerm())

	def parseArgList(self):
		ret = []

		self.expect(PAREN, "(")

		while not self.match(PAREN, ")"):
			ret.append(self.parseExpr())
			if not self.accept(COMMA):
				break

		self.expect(PAREN, ")")

		return ret

	def parseCall(self, left):
		if type(left) == IdentifierNode and self.match(PAREN, "("):
			return CallNode(left, self.parseArgList())
		else:
			return left

	def parseTerm(self):
		if self.match(TokenType.NUMBER):
			return NumberNode(float(self.nextToken()[1]))
		elif self.accept(TokenType.PAREN, "("):
			stmt = self.parseExpr()
			self.expect(PAREN, ")")
			return stmt
		elif self.match(TokenType.STRING):
			return StringNode(self.nextToken()[1])
		elif self.match(TokenType.IDENTIFIER):
			return IdentifierNode(self.nextToken()[1])
		else:
			error("pk tu fais ça")
			return None