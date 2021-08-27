from errors.error import Error
from lexing.tokens import Token, TokenType
from typing import List, Tuple
from lexing.source_pos import SourcePosition

class Lexer:
    def __init__(self, source: str, file_name: str):
        self.source = source
        self.file_name = file_name
        self.position = SourcePosition(source, file_name)

    def make_token(self) -> Tuple[Token, Error]:
        self.position.advance()
        return Token(TokenType.EOF, self.position.copy(), self.position.copy()), None

    def tokenize(self) -> Tuple[List[Token], Error]:
        """
        Returns a list of tokens from the source code.
        """
        tokens = list()

        while self.position.char != None:
            # If the current character is whitespace, then simply skip it.
            if self.position.char.isspace():
                self.position.advance()
                continue

            token, error = self.make_token()
            if error:
                return [], error

            tokens.append(token)

        return tokens, None
