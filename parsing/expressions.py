from lexing.source_pos import SourcePosition
from lexing.tokens import Token

class Expression:
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition):
        self.start_pos = start_pos
        self.end_pos = end_pos

class BinaryExpression(Expression):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, left: Expression, operator: Token, right: Expression):
        super().__init__(start_pos, end_pos)
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(Expression):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, operator: Token, right: Expression):
        super().__init__(start_pos, end_pos)
        self.operator = operator
        self.right = right

class LiteralExpression(Expression):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, literal: Token):
        super().__init__(start_pos, end_pos)
        self.literal = literal

class GroupedExpression(Expression):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, expression: Expression):
        super().__init__(start_pos, end_pos)
        self.expression = expression