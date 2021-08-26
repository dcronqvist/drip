from lexing.tokens import Token
from typing import List, Tuple
from lexing.source_pos import SourcePosition

class Lexer:
    def __init__(self, source: str, file_name: str):
        self.source = source
        self.file_name = file_name
        self.position = SourcePosition(source, file_name)

    def make_token(self) -> Token:
        pass

    def tokenize(self) -> List[Token]:
        """
        Returns a list of tokens from the source code.
        """

        tokens = list()

        while self.position.char != None:

            # If the current character is whitespace, then simply skip it.
            if self.position.char.isspace():
                self.position.advance()
                continue
