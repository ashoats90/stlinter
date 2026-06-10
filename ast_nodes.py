from dataclasses import dataclass

@dataclass
class Program:
    statements: list

@dataclass
class VarDecl:
    name: str
    type_name: str
    line: int
    col: int