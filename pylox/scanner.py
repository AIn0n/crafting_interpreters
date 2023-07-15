from token import Token
from tokenTypes import Token_type
from errors import error
from string import digits, ascii_letters
from keywords import keywords


def is_alpha(c: str) -> bool:
    return c in ascii_letters or c == "_"


def is_alpha_numeric(c: str) -> bool:
    return is_alpha(c) or c in digits


class Scanner:
    def __init__(self, src: str) -> None:
        self.src = src
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 0

    def identifier(self):
        while is_alpha_numeric(self.peek()):
            self.advance()

        text = self.src[self.start : self.current]
        type_ = keywords[text] if text in keywords else Token_type.IDENTIFIER

        self.add_token(type_, text)

    # TODO: refactor this shit to make it more versatile
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.src):
            return "\0"
        return self.src[self.current + 1]

    def number(self):
        while self.peek() in digits:
            self.advance()

        if self.peek() == "." and self.peek_next() in digits:
            # consume the dot
            self.advance()

        while self.peek() in digits:
            self.advance()

        self.add_token(Token_type.NUMBER, float(self.src[self.start : self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error(self.line, "unterminated string")
            return

        # pick the closing "
        self.advance()

        # plus minus one below is trimming quote signs
        # in the future it is the place where we can add unescape \
        self.add_token(Token_type.STRING, self.src[self.start + 1 : self.current - 1])

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.src[self.current]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.src[self.current] != expected:
            return False
        self.current += 1
        return True

    def is_at_end(self) -> bool:
        return len(self.src) <= self.current

    def advance(self) -> str:
        char = self.src[self.current]
        self.current += 1
        return char

    def add_token(self, ttype: Token_type, literal=None) -> None:
        text = self.src[self.start : self.current]
        self.tokens.append(Token(ttype, text, literal, self.line))

    def scan_token(self) -> Token:
        char = self.advance()
        match char:
            case "(":
                self.add_token(Token_type.LEFT_PAREN)
            case ")":
                self.add_token(Token_type.RIGHT_PAREN)
            case "{":
                self.add_token(Token_type.LEFT_BRACE)
            case "}":
                self.add_token(Token_type.RIGHT_BRACE)
            case ",":
                self.add_token(Token_type.COMMA)
            case ".":
                self.add_token(Token_type.DOT)
            case "-":
                self.add_token(Token_type.MINUS)
            case "+":
                self.add_token(Token_type.PLUS)
            case ";":
                self.add_token(Token_type.SEMICOLON)
            case "*":
                self.add_token(Token_type.STAR)
            case "!":
                self.add_token(
                    Token_type.BANG_EQUAL if self.match("=") else Token_type.BANG
                )
            case "=":
                self.add_token(
                    Token_type.EQUAL_EQUAL if self.match("=") else Token_type.EQUAL
                )
            case "<":
                self.add_token(
                    Token_type.LESS_EQUAL if self.match("=") else Token_type.LESS
                )
            case ">":
                self.add_token(
                    Token_type.GREATER_EQUAL if self.match("=") else Token_type.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(Token_type.SLASH)
            case "\r" | " " | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case c if c in digits:
                self.number()
            case c if is_alpha(c):
                self.identifier()
            case default:
                error(self.line, "unexpected character")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return self.tokens
