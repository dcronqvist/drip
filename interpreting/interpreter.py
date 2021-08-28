from interpreting.statements import AssignmentStatement, ExpressionStatement, Statement
from typing import Tuple
from interpreting.values import Boolean, Number, String, ValueNode
from lexing.tokens import TokenType
from parsing.expressions import BinaryExpression, Expression, GroupedExpression, IdentifierExpression, LiteralExpression, UnaryExpression
from errors.error import Error, RuntimeError

class Interpreter:
    def __init__(self):
        self.globals = dict()

    def interpret(self, statement: Statement) -> Tuple[ValueNode, Error]:
        return self.visit(statement)

    def visit(self, statement: Statement) -> Tuple[ValueNode, Error]:
        method_name = f"visit_{statement.__class__.__name__}"

        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(statement)
        
        return None, RuntimeError(statement.start_pos, statement.end_pos, f"No visit method '{method_name}' implemented.")

    def visit_LiteralExpression(self, expression: LiteralExpression) -> Tuple[ValueNode, Error]:
        if expression.literal.token_type == TokenType.NUMBER:
            return Number(expression.literal.value), None
        elif expression.literal.token_type == TokenType.STRING:
            return String(expression.literal.value), None
        elif expression.literal.token_type == TokenType.BOOLEAN:
            return Boolean(expression.literal.value), None
        
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
        elif expression.operator.token_type == TokenType.AND:
            result = left.andand(right)
        elif expression.operator.token_type == TokenType.OR:
            result = left.oror(right)


        if result == None:
            return None, RuntimeError(expression.start_pos, expression.end_pos, f"Invalid operation {expression.operator.token_type.value} between types {left.__class__.__name__} and {right.__class__.__name__}")
        else:
            return result, None

    def visit_UnaryExpression(self, expression: UnaryExpression) -> Tuple[ValueNode, Error]:
        value, error = self.visit(expression.right)
        if error:
            return None, error

        result = None
        if expression.operator.token_type == TokenType.MINUS:
            result = value.negate()
        elif expression.operator.token_type == TokenType.NOT:
            result = value.notnot()

        if result == None:
            return None, RuntimeError(expression.start_pos, expression.end_pos, f"Invalid operation {expression.operator.token_type.value} on type {value.__class__.__name__}")
        else:
            return result, None


    def visit_GroupedExpression(self, expression: GroupedExpression) -> Tuple[ValueNode, Error]:
        return self.visit(expression.expression)

    def visit_ExpressionStatement(self, expression: ExpressionStatement) -> Tuple[ValueNode, Error]:
        return self.visit(expression.expression)

    def visit_IdentifierExpression(self, expression: IdentifierExpression) -> Tuple[ValueNode, Error]:
        if expression.identifier.value in self.globals:
            return self.globals[expression.identifier.value], None
        else:
            return None, RuntimeError(expression.start_pos, expression.end_pos, f"Identifier {expression.identifier.value} not found in global scope.")

    def visit_AssignmentStatement(self, expression: AssignmentStatement) -> Tuple[ValueNode, Error]:
        value, error = self.visit(expression.expression)
        if error:
            return None, error

        self.globals[expression.identifier.value] = value

        return value, None


        

        

