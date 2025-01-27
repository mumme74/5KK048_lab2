# an example file added to repository for course 5KK048 course

# a quick expression based calculatror using a lexer and a recursive descent parser-

# The different types of tokens
class Type:
    Number = 'num'
    Neg    = '-'
    Add    = '+'
    Mul    = '*'
    Div    = '/'
    LParen = '('
    RParen = ')'
    Expon  = '^'
    Digit  = '0-9'
    Dot    = '.'

class Token:
    def __init__(self, type:Type, text:str):
        self.type = type
        self.text = text

class ParseError(Exception): pass
class ParseEof(Exception): pass

def lex(src:str):
    tokens = []
    i = 0
    while i < len(src):
        ch = src[i]
        match ch:
            case '(':
                tokens.append(Token(Type.LParen, ch))
            case ')':
                tokens.append(Token(Type.RParen, ch))
            case '-':
                tokens.append(Token(Type.Neg, ch))
            case '+':
                tokens.append(Token(Type.Add, ch))
            case '*':
                tokens.append(Token(Type.Mul, ch))
            case '/':
                tokens.append(Token(Type.Div, ch))
            case '^':
                tokens.append(Token(Type.Expon, ch))
            case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
                tokens.append(Token(Type.Digit, ch))
            case '.'|',':
                tokens.append(Token(Type.Dot), '.')
            case _:
                raise ParseError(f"Unexpected '{ch}' in column {i}")
        i += 1

    return tokens

class AstNode:
    def __init__(self, tok:Token|None = None, value:float|None = None):
        self.left = None
        self.right = None
        self.tok = tok
        self.op_fn = None
        self._value = value

    def value(self):
        if self.op_fn:
            return self.op_fn()
        elif self._value is not None:
            return self._value
        else:
            return self.left.value()

    def number(self):
        assert self.tok.type == Type.Number
        return float(self.tok.text)

# EBNF grammar, hopefully I got it right?!
# expression => term, { add_op, term }
# term       => factor, { mul_op, factor }
# factor     => primary, ['^', factor ]
# primary    => [ sign ], ( number | '(', expression, ')' )
# number     => 0-9, {0-9}, ['.', {0-9}]
# add_op     => '+' | '-'
# mul_op     => '*' / '/'
# sign       => '+' | '-'


class Parse:
    def __init__(self, src:str):
        self.tokens = lex(src)
        self._idx = 0
        self.ast = self._expression()

    def _cur(self):
        if self._idx < len(self.tokens):
            return self.tokens[self._idx]
        raise ParseEof()

    def _next(self) -> Token:
        self._idx += 1
        return self._cur()

    def _expect(self, type: list[Type]):
        try:
            tok = self._next()
            if tok.type != type:
                self._idx -= 1
                raise ParseError(f"Expected a '{type}' got a {tok.type}")
        except ParseEof:
            raise ParseError(f"Expected a '{type}' is at end")

    # expression => term, { add_op, term }
    def _expression(self):
        left = self._term()
        try:
            op = self._add_op()
            right = self._term()
        except ParseError:
            return left
        else:
            op.left = left
            op.right = right
            return op

    # term       => factor, { mul_op, factor }
    def _term(self):
        left = self._factor()
        try:
            mul_op = self._mul_op()
            right = self._factor()
        except ParseError:
            return left
        else:
            mul_op.left = left
            mul_op.right = right
            return mul_op

    # factor     => primary, ['^', factor ]
    def _factor(self):
        left = self._primary()
        try:
            self._expect([Type.Expon])
            right = self._factor()
        except ParseError:
            return left
        else:
            node = AstNode(Type.Expon)
            node.op_fn = lambda _: node.left.value() ** node.right.value()
            node.left = left
            node.right = right
            return node

    # primary    => [ sign ], ( number | '(', expression, ')' )
    def _primary(self):
        try:
            sign = self._sign()
        except ParseError:
            pass

        tok = self._next()
        if tok.type == Type.Number:
            if sign:
                sign.left = self._number()
                return sign
            return self._number()
        elif tok.type == Type.LParen:
            expr = self._expression()
            self._expect([Type.RParen])
            if sign:
                sign.left = expr
                return sign
            return expr

    # number     => 0-9, {0-9}, ['.', {0-9}]
    def _number(self):
        self.expect([Type.Digit])
        start = cur = self._cur()
        digits = [cur.text]
        cur = self._next()

        while cur.type == Type.Digit:
            digits.append(cur.text)
            cur = self._next()

        if cur.type == Type.Dot:
            digits.append(cur.text)
        cur = self._next()

        while cur.type == Type.Digit:
            digits.append(cur.text)
            cur = self._next()

        node = AstNode(start)
        node.value = float(''.join(digits))
        return node


    # add_op     => '+' | '-'
    def add_op(self):
        self._expect([Type.Add,Type.Neg])
        tok = self._cur()
        node = AstNode(tok)
        if tok.type == Type.Add:
            node.op_fn = lambda _: node.left.value() + node.right.value()
        else:
            node.op_fn = lambda _: node.left.value() - node.right.value()
        return node

    # mul_op     => '*' / '/'
    def add_op(self):
        self._expect([Type.Mul,Type.Div])
        tok = self._cur()
        node = AstNode(tok)
        if tok.type == Type.Mul:
            node.op_fn = lambda _: node.left.value() * node.right.value()
        else:
            node.op_fn = lambda _: node.left.value() / node.right.value()
        return node

    # sign       => '+' | '-'
    def sign(self):
        self._expect([Type.Add,Type.Neg])
        tok = self._cur()
        node = AstNode(tok)
        if tok.type == Type.Add:
            node.op_fn = lambda _: node.left.value()
        else:
            node.op_fn = lambda _: node.left.value() * -1.0
        return node

def main():
    print("Welcome to calculator")
    while True:
        inp = input("Type a mathematical expression: ")
        if not inp:
            break
        try:
            parser = Parse(inp)
            vlu = parser.ast.value()
            print(f"{vlu}")
        except ParseError as e:
            print(f"Error: {e}")
        except ParseEof:
            pass
    print("Exiting calculator")

if __name__ == "__main__":
    main()
