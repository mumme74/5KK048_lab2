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
            case _:
                j = i
                while j < len(src):
                    ch = src[j]
                    if not ch.isnumeric() and not ch == '.':
                        break
                    j += 1
                if i == j:
                    raise ParseError(f"Unexpected '{src[i]}' in column {i}")
                else:
                    tokens.append(Token(Type.Number, src[i:j]))
                    i = j - 1
        i += 1

    return tokens

# EBNF grammar
# start      => expression, [{expression}]
# expression => expression, add_op, term
#             | term
# term       => term, mul_op, factor
#             | factor
# factor     => value '^' factor
#             | value
# value      => [sign], number
# sign       => '+' | '-'
# add_op     => '+' | '-'
# mul_op     => '/' | '*'
class AstNode:
    def __init__(self, tok:Token):
        self.left = None
        self.right = None
        self.tok = tok

class Parse:
    def __init__(self, src:str):
        self.tokens = lex(src)
        self._idx = 0
        self.ast = AstNode()

    def _next(self) -> Token:
        self._idx += 1
        if self._idx < len(self.tokens):
            return self.tokens[self._idx]
        raise ParseEof()

    def _expect(self, type: Type):
        try:
            tok = self._next()
            if tok.type != type:
                raise ParseError(f"Expected a '{type}' got a {tok.type}")
        except ParseEof:
            raise ParseError(f"Expected a '{type}' is at end")



    def _start(self):
        self._expression()
