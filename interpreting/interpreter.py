from typing import Tuple
from interpreting.values import Float, Integer, ValueNode
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
        if expression.literal.token_type == TokenType.INTEGER:
            return Integer(expression.literal.value), None
        elif expression.literal.token_type == TokenType.FLOAT:
            return Float(expression.literal.value), None
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
        

        if not result:
            return None, RuntimeError(expression.start_pos, expression.end_pos, f"Invalid operation {expression.operator.token_type.value} between types {left.__class__.__name__} and {right.__class__.__name__}")
        else:
            return result, None

    def visit_GroupedExpression(self, expression: GroupedExpression) -> Tuple[ValueNode, Error]:
        return self.visit(expression.expression)


        

        

