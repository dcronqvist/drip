from errors.error import Error, SyntaxError
from lexing.tokens import Token, TokenType
from typing import List, Tuple
from lexing.source_pos import SourcePosition

class Lexer:
    def __init__(self, source: str, file_name: str):
        self.source = source
        self.file_name = file_name
        self.position = SourcePosition(source, file_name)
        self.digits = "0123456789"
        self.alphanumeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        self.keywords = {
            "and": TokenType.AND,
            "or": TokenType.OR,
            "not": TokenType.NOT,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "null": TokenType.NULL,
        }

    def consume(self, expected: str, message: str = None) -> Error:
        """
        Consumes the next character, if it is the expected character, otherwise returns an error.
        """
        if self.match(expected):
            return None

        if not message:
            return SyntaxError(self.position.copy(), self.position.copy(), f"Expected {expected} but found {self.position.char}")

        return SyntaxError(self.position.copy(), self.position.copy(), message)

    def match(self, character: str) -> bool:
        """
        Returns True if the current character is the character specified. Also advances one character if it is True.
        """
        if self.position.char == character:
            self.position.advance()
            return True

        return False

    def make_number(self) -> Tuple[Token, Error]:
        """
        Returns either a FLOAT or INTEGER token.
        In the case of too many dots (> 1), an error is returned.
        """
        start_position = self.position.copy()

        number = ""
        dots = 0

        digits_and_dot = self.digits + "."

        while self.position.char != None and self.position.char in digits_and_dot:
            if self.position.char == ".":
                dots += 1

            number += self.position.char
            self.position.advance()

        if dots == 0:
            return Token(TokenType.INTEGER, start_position, self.position.copy(), value=int(number)), None
        elif dots == 1:
            return Token(TokenType.FLOAT, start_position, self.position.copy(), value=float(number)), None

        return None, SyntaxError(start_position, self.position.copy(), f"Invalid number format: {number}")

    def make_string(self, string_terminator: str) -> Tuple[Token, Error]:
        s = ""
        self.position.advance()

        while self.position.char != None and self.position.char != string_terminator:
            s += self.position.char
            self.position.advance()

        error = self.consume(string_terminator, "Missing string terminator")
        if error:
            return None, error

        return Token(TokenType.STRING, self.position.copy(), self.position.copy(), value=s), None

    def make_identifier_keyword(self) -> Tuple[Token, Error]:
        start_position = self.position.copy()

        s = ""

        while self.position.char != None and self.position.char in self.alphanumeric:
            s += self.position.char
            self.position.advance()

        if s in self.keywords:
            return Token(self.keywords[s], start_position, self.position.copy()), None

        return Token(TokenType.IDENTIFIER, start_position, self.position.copy(), value=s), None

    def make_token(self) -> Tuple[Token, Error]:
        if self.position.char in self.digits:
            return self.make_number()

        if self.position.char in self.alphanumeric:
            return self.make_identifier_keyword()

        elif self.match("+"):
            return Token(TokenType.PLUS, self.position.copy(), self.position.copy()), None
        elif self.match("-"):
            return Token(TokenType.MINUS, self.position.copy(), self.position.copy()), None

        elif self.match("*"):
            return Token(TokenType.STAR, self.position.copy(), self.position.copy()), None

        elif self.match("/"):
            return Token(TokenType.SLASH, self.position.copy(), self.position.copy()), None

        elif self.match("%"):
            return Token(TokenType.PERCENT, self.position.copy(), self.position.copy()), None

        elif self.match("("):
            return Token(TokenType.LPAREN, self.position.copy(), self.position.copy()), None

        elif self.match(")"):
            return Token(TokenType.RPAREN, self.position.copy(), self.position.copy()), None

        elif self.match("["):
            return Token(TokenType.LBRACKET, self.position.copy(), self.position.copy()), None

        elif self.match("]"):
            return Token(TokenType.RBRACKET, self.position.copy(), self.position.copy()), None

        elif self.match("{"):
            return Token(TokenType.LBRACE, self.position.copy(), self.position.copy()), None

        elif self.match("}"):
            return Token(TokenType.RBRACE, self.position.copy(), self.position.copy()), None

        elif self.match(";"):
            return Token(TokenType.SEMICOLON, self.position.copy(), self.position.copy()), None

        elif self.match(":"):
            return Token(TokenType.COLON, self.position.copy(), self.position.copy()), None

        elif self.match("="):
            if self.match("="):
                return Token(TokenType.EQUAL_EQUAL, self.position.copy(), self.position.copy()), None
            else:
                return Token(TokenType.EQUALS, self.position.copy(), self.position.copy()), None

        elif self.position.char in ["'", '"']:
            return self.make_string(self.position.char)
        else:
            return None, SyntaxError(self.position.copy(), self.position.copy(), f"Invalid character: {self.position.char}")

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
