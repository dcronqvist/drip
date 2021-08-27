from __future__ import annotations
from errors.error import Error
from typing import Tuple


class ValueNode:
    def __init__(self, value):
        self.value = value

    def plus(self, other: ValueNode) -> ValueNode:
        return None

    def minus(self, other: ValueNode) -> ValueNode:
        return None

    def star(self, other: ValueNode) -> ValueNode:
        return None

    def slash(self, other: ValueNode) -> ValueNode:
        return None

    def percent(self, other: ValueNode) -> ValueNode:
        return None

    def eqeq(self, other: ValueNode) -> ValueNode:
        return None

    def neeq(self, other: ValueNode) -> ValueNode:
        return None

    def gt(self, other: ValueNode) -> ValueNode:
        return None

    def lt(self, other: ValueNode) -> ValueNode:
        return None

    def gte(self, other: ValueNode) -> ValueNode:
        return None

    def lte(self, other: ValueNode) -> ValueNode:
        return None

    def andand(self, other: ValueNode) -> ValueNode:
        return None

    def oror(self, other: ValueNode) -> ValueNode:
        return None

    def notnot(self: ValueNode) -> ValueNode:
        return None


class Float(ValueNode):
    def __init__(self, value):
        super().__init__(value)

    def plus(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        elif isinstance(other, Float):
            return Float(self.value + other.value)

        return None

    def minus(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value - other.value)
        elif isinstance(other, Float):
            return Float(self.value - other.value)

        return None

    def star(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, Float):
            return Float(self.value * other.value)
        
        return None

    def slash(self, other: ValueNode) -> ValueNode:
        if isinstance(other, (Integer, Float)):
            return Float(self.value / other.value)


class Integer(ValueNode):
    def __init__(self, value):
        super().__init__(value)

    def plus(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        elif isinstance(other, Float):
            return Float(self.value + other.value)

        return None

    def minus(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value - other.value)
        elif isinstance(other, Float):
            return Float(self.value - other.value)

        return None

    def star(self, other: ValueNode) -> ValueNode:
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, Float):
            return Float(self.value * other.value)
        
        return None

    def slash(self, other: ValueNode) -> ValueNode:
        if isinstance(other, (Integer, Float)):
            return Float(self.value / other.value)

        return None