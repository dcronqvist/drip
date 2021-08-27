from enum import Enum
from lexing.source_pos import SourcePosition

class TokenType(Enum):
    # Single-character tokens.
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    BANG = "!"

    # Literal values.
    INTEGER = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOL"

    # End of file.
    EOF = 'EOF'

class Token:
    def __init__(self, token_type: TokenType, start_pos: SourcePosition, end_pos: SourcePosition, value=None):
        self.token_type = token_type
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'<{self.token_type.value}, {self.value}>'
        else:
            return f'<{self.token_type.value}>'
