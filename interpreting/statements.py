from lexing.tokens import Token
from parsing.expressions import Expression
from lexing.source_pos import SourcePosition

class Statement:
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition):
        self.start_pos = start_pos
        self.end_pos = end_pos

class ExpressionStatement(Statement):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, expression: Expression):
        super().__init__(start_pos, end_pos)
        self.expression = expression

class AssignmentStatement(Statement):
    def __init__(self, start_pos: SourcePosition, end_pos: SourcePosition, identifier: Token, expression: Expression):
        super().__init__(start_pos, end_pos)
        self.identifier = identifier
        self.expression = expression