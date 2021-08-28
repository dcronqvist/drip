from enum import Enum
from lexing.source_pos import SourcePosition

class TokenType(Enum):
    # Single-character tokens.
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    POW = "^"

    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COLON = ":"
    EQUALS = "="

    # Two-character tokens.
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="

    # Literal values.
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"

    # Identifiers
    IDENTIFIER = "IDENTIFIER"

    # Keywords
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"

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
            return f'<{self.token_type.value}:{self.value}>'
        else:
            return f'<{self.token_type.value}>'
