from tokenTypes import Token_type


class Token:
    def __init__(self, ttype: Token_type, lexeme: str, literal, line: int):
        self.ttype = ttype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"{self.ttype} {self.lexeme} {self.literal}"
