from dataclasses import dataclass

@dataclass
class Program:
    statements: list

@dataclass
class VarDecl:
    name: str
    type_name: str
    line: int
    column: int

@dataclass
class Assignment:
    target: str
    value: object
    line: int
    column: int

@dataclass
class BooleanLiteral:
    value: bool
    line: int
    column: int

@dataclass
class StringLiteral:
    value: str
    line: int
    column: int

@dataclass
class NumberLiteral:
    value: str
    line: int
    column: int

@dataclass
class Identifier:
    value: str
    line: int
    column: int

@dataclass
class IfStatement:
    condition: object
    body: list
    line: int
    column: int