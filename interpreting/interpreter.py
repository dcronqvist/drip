from typing import Tuple
from interpreting.values import Number, ValueNode
from lexing.tokens import TokenType
from parsing.expressions import BinaryExpression, Expression, GroupedExpression, LiteralExpression
from errors.error import Error, RuntimeError

class Interpreter:
    def __init__(self, expression: Expression):
        self.expression = expression

    def interpret(self):
        return self.visit(self.expression)

    def visit(self, expression: Expression) -> Tuple[ValueNode, Error]:
        method_name = f"visit_{expression.__class__.__name__}"

        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(expression)
        
        return None, RuntimeError(expression.start_pos, expression.end_pos, f"No visit method '{method_name}' implemented.")

    def visit_LiteralExpression(self, expression: LiteralExpression) -> Tuple[ValueNode, Error]:
        if expression.literal.token_type == TokenType.NUMBER:
            return Number(expression.literal.value), None
        return None, RuntimeError(expression.start_pos, expression.end_pos, f"No visitor method for literal {expression.literal.token_type}")

    def visit_BinaryExpression(self, expression: BinaryExpression) -> Tuple[ValueNode, Error]:
        left, left_error = self.visit(expression.left)
        if left_error:
            return None, left_error

        right, right_error = self.visit(expression.right)
        if right_error:
            return None, right_error

        result = None

        if expression.operator.token_type == TokenType.PLUS:
            result = left.plus(right)
        elif expression.operator.token_type == TokenType.MINUS:
            result = left.minus(right)
        elif expression.operator.token_type == TokenType.STAR:
            result = left.star(right)
        elif expression.operator.token_type == TokenType.SLASH:
            result = left.slash(right)
        elif expression.operator.token_type == TokenType.PERCENT:
            result = left.percent(right)
        elif expression.operator.token_type == TokenType.POW:
            result = left.pow(right)
        elif expression.operator.token_type == TokenType.EQUAL_EQUAL:
            result = left.eqeq(right)
        elif expression.operator.token_type == TokenType.NOT_EQUAL:
            result = left.neeq(right)
        elif expression.operator.token_type == TokenType.GREATER_THAN:
            result = left.gt(right)
        elif expression.operator.token_type == TokenType.GREATER_THAN_EQUAL:
            result = left.gte(right)
        elif expression.operator.token_type == TokenType.LESS_THAN:
            result = left.lt(right)
        elif expression.operator.token_type == TokenType.LESS_THAN_EQUAL:
            result = left.lte(right)

        if not result:
            return None, RuntimeError(expression.start_pos, expression.end_pos, f"Invalid operation {expression.operator.token_type.value} between types {left.__class__.__name__} and {right.__class__.__name__}")
        else:
            return result, None

    def visit_GroupedExpression(self, expression: GroupedExpression) -> Tuple[ValueNode, Error]:
        return self.visit(expression.expression)


        

        

