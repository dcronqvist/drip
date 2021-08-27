from os import error
from parsing.expressions import BinaryExpression, Expression, GroupedExpression, LiteralExpression, UnaryExpression
from errors.error import Error, SyntaxError
from typing import List, Tuple
from lexing.tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]

    def advance(self):
        self.index += 1

        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

        return self.current_token

    def consume(self, token_type: TokenType, message: str = None) -> Error:
        if not self.match(token_type):
            if not message:
                return SyntaxError(self.current_token.start_pos, self.current_token.end_pos, f"Expected '{token_type.value}' but found '{self.current_token.value}'")

    def match(self, token_type: TokenType) -> bool:
        if self.current_token != None and self.current_token.token_type == token_type:
            self.advance()
            return True
        return False

    def match_oneof(self, token_types: List[TokenType]) -> bool:
        if self.current_token != None and self.current_token.token_type in token_types:
            self.advance()
            return True
        return False

    def previous(self) -> Token:
        return self.tokens[self.index - 1]

    def parse(self) -> Tuple[Expression, Error]:
        return self.expression()

    def expression(self) -> Tuple[Expression, Error]:
        return self.term()

    def term(self) -> Tuple[Expression, Error]:
        factor, error = self.factor()
        if error:
            return None, error

        if self.match_oneof([TokenType.PLUS, TokenType.MINUS]):
            operator = self.previous()
            right, error = self.factor()
            if error:
                return None, error
            factor = BinaryExpression(factor.start_pos.copy(), right.end_pos.copy(), factor, operator, right)

        return factor, None

    def factor(self) -> Tuple[Expression, Error]:
        unary, error = self.unary()
        if error:
            return None, error

        if self.match_oneof([TokenType.STAR, TokenType.SLASH, TokenType.POW, TokenType.PERCENT]):
            operator = self.previous()
            right, error = self.unary()
            if error:
                return None, error

            unary = BinaryExpression(unary.start_pos.copy(), right.end_pos.copy(), unary, operator, right)
        else:
            return None, SyntaxError(self.current_token.start_pos.regress(), self.current_token.end_pos.regress(), f"Expected '*' or '/' but found '{self.current_token.token_type.value}'")

        return unary, None

    def unary(self) -> Tuple[Expression, Error]:
        if self.match_oneof([TokenType.NOT, TokenType.MINUS]):
            operator = self.previous()
            right, error = self.unary()
            if error:
                return None, error
            return UnaryExpression(operator.start_pos.copy(), right.end_pos.copy(), operator, right), None
        else:
            return self.primary()

    def primary(self) -> Tuple[Expression, Error]:

        if self.match(TokenType.LPAREN):
            expr, err = self.expression()
            if err:
                return None, err

            error = self.consume(TokenType.RPAREN, "Expected ')'")
            if error:
                return None, error
            return GroupedExpression(expr.start_pos.copy(), expr.end_pos.copy(), expr), None

        if self.match_oneof([TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NULL]):
            prev = self.previous()
            return LiteralExpression(prev.start_pos.copy(), prev.end_pos.set_position(prev.end_pos.line, prev.end_pos.column, prev.end_pos.index).copy(), prev), None
        else:
            return None, SyntaxError(self.previous().start_pos, self.previous().end_pos, f"Expected literal value but found '{self.previous().value}'")
