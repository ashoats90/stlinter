import pytest

from stlinter.tokenizer import Tokenizer
from stlinter.parser import Parser, ParserError
from stlinter.ast_nodes import Program, VarDecl, Assignment, BooleanLiteral, StringLiteral, NumberLiteral, Identifier


def parse_source(source: str) -> Program:
    tokens = Tokenizer(source).tokenize()
    return Parser(tokens).parse()


def test_parses_single_var_declaration():
    program = parse_source("""
VAR
    MotorRun : BOOL;
END_VAR
""")

    assert program == Program(
        statements=[
            VarDecl("MotorRun", "BOOL", line=3, column=5)
        ]
    )


def test_parses_multiple_var_declarations():
    program = parse_source("""
VAR
    MotorRun : BOOL;
    Count : INT;
END_VAR
""")

    assert program == Program(
        statements=[
            VarDecl("MotorRun", "BOOL", line=3, column=5),
            VarDecl("Count", "INT", line=4, column=5),
        ]
    )


def test_missing_colon_raises_parser_error():
    source = """
VAR
    MotorRun BOOL;
END_VAR
"""

    with pytest.raises(ParserError):
        parse_source(source)


def test_missing_semicolon_raises_parser_error():
    source = """
VAR
    MotorRun : BOOL
END_VAR
"""

    with pytest.raises(ParserError):
        parse_source(source)

def test_parses_boolean_assignment():
    program = parse_source("MotorRun := TRUE;")

    assert program == Program(
        statements=[
            Assignment(
                target="MotorRun",
                value=BooleanLiteral(True, line=1, column=13),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_false_assignment():
    program = parse_source("MotorRun := FALSE;")

    assert program == Program(
        statements=[
            Assignment(
                target="MotorRun",
                value=BooleanLiteral(False, line=1, column=13),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_string_assignment():
    program = parse_source("MotorName := 'Motor1';")

    assert program == Program(
        statements=[
            Assignment(
                target="MotorName",
                value=StringLiteral("Motor1", line=1, column=14),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_numerical_assignment():
    program = parse_source("MotorNum := 1;")

    assert program == Program(
        statements=[
            Assignment(
                target="MotorNum",
                value=NumberLiteral("1", line=1, column=13),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_identifier_assignment():
    program = parse_source("MotorRun := StartButton;")

    assert program == Program(
        statements=[
            Assignment(
                target="MotorRun",
                value=Identifier("StartButton", line=1, column=13),
                line=1,
                column=1,
            )
        ]
    )

def test_assignment_missing_expression_raises():
    with pytest.raises(ParserError):
        parse_source("MotorRun := ;")

def test_assignment_missing_semicolon_raises():
    with pytest.raises(ParserError):
        parse_source("MotorRun := TRUE")