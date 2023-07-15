from token import Token
from tokenTypes import Token_type
from errors import error


class Scanner:
    def __init__(self, src: str) -> None:
        self.src = src
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 0

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
            case default:
                error(self.line, "unexpected character")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
