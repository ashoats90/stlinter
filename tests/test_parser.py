import pytest

from stlinter.tokenizer import Tokenizer
from stlinter.parser import Parser, ParserError
from stlinter.ast_nodes import Program, VarDecl


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