from enum import Enum

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
    def __init__(self, token_type: TokenType, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'<{self.token_type}, {self.value}>'
        else:
            return f'<{self.token_type}>'
