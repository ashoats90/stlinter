import pytest

from stlinter.tokenizer import Tokenizer
from stlinter.parser import Parser, ParserError
from stlinter.ast_nodes import Program, VarDecl, Assignment, BooleanLiteral, StringLiteral, NumberLiteral, Identifier, IfStatement, BinaryExpression


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

def test_parses_if_statement_with_assignment_body():
    program = parse_source("""
IF MotorRun THEN
    Message := 'Running';
END_IF;
""")
    
    assert program == Program(
        statements=[
            IfStatement(
                condition=Identifier("MotorRun", line=2, column=4),
                body=[
                    Assignment(
                        target="Message",
                        value=StringLiteral("Running", line=3, column=16),
                        line=3,
                        column=5,
                    )
                ],
                line=2,
                column=1,
            )
        ]
    )

def test_if_missing_then_raises_parser_error():
    with pytest.raises(ParserError):
        parse_source("""
IF MotorRun
    Message := 'Running';
END_IF;
""")


def test_if_missing_end_if_raises_parser_error():
    with pytest.raises(ParserError):
        parse_source("""
IF MotorRun THEN
    Message := 'Running';
""")


def test_if_missing_semicolon_after_end_if_raises_parser_error():
    with pytest.raises(ParserError):
        parse_source("""
IF MotorRun THEN
    Message := 'Running';
END_IF
""")
        
def test_parses_nested_if_statement():
    program = parse_source("""
IF MotorRun THEN
    IF StartButton THEN
        Message := 'Running';
    END_IF;
END_IF;
""")

    assert len(program.statements) == 1

def test_parses_if_condition_with_comparison():
    program = parse_source("""
IF Count >= 10 THEN
    MotorRun := TRUE;
END_IF;
""")
    
    assert program == Program(
        statements=[
            IfStatement(
                condition=BinaryExpression(
                    left=Identifier("Count", line=2, column=4),
                    operator=">=",
                    right=NumberLiteral("10", line=2, column=13),
                    line=2,
                    column=4,
                ),
                body=[
                    Assignment(
                        target="MotorRun",
                        value=BooleanLiteral(True, line=3, column=17),
                        line=3,
                        column=5,
                    )
                ],
                line=2,
                column=1,
            )
        ]
    )

def test_parses_assignment_with_addition_expression():
    program = parse_source("Count := Count + 1;")

    assert program == Program(
        statements=[
            Assignment(
                target="Count",
                value=BinaryExpression(
                    left=Identifier("Count", line=1, column=10),
                    operator="+",
                    right=NumberLiteral("1", line=1, column=18),
                    line=1,
                    column=10,
                ),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_precedence_addition_multiplication():
    program = parse_source("Result := A + B * C;")

    assert program == Program(
        statements=[
            Assignment(
                target="Result",
                value=BinaryExpression(
                    left=Identifier("A", line=1, column=11),
                    operator="+",
                    right=BinaryExpression(
                        left=Identifier("B", line=1, column=15),
                        operator="*",
                        right=Identifier("C", line=1, column=19),
                        line=1,
                        column=15,
                    ),
                    line=1,
                    column=11,
                ),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_precedence_comparison_addition_multiplication():
    program = parse_source("Result := A + B >= C * D;")

    assert program == Program(
        statements=[
            Assignment(
                target="Result",
                value=BinaryExpression(
                    left=BinaryExpression(
                        left=Identifier("A", line=1, column=11),
                        operator="+",
                        right=Identifier("B", line=1, column=15),
                        line=1,
                        column=11,
                    ),
                    operator=">=",
                    right=BinaryExpression(
                        left=Identifier("C", line=1, column=20),
                        operator="*",
                        right=Identifier("D", line=1, column=24),
                        line=1,
                        column=20,
                    ),
                    line=1,
                    column=11,
                ),
                line=1,
                column=1,
            )
        ]
    )

def test_parses_parenthesized_expression_precedence():
    program = parse_source("Result := (A + B) * C;")

    assert program == Program(
        statements=[
            Assignment(
                target="Result",
                value=BinaryExpression(
                    left=BinaryExpression(
                        left=Identifier("A", line=1, column=12),
                        operator="+",
                        right=Identifier("B", line=1, column=16),
                        line=1,
                        column=12,
                    ),
                    operator="*",
                    right=Identifier("C", line=1, column=21),
                    line=1,
                    column=12,
                ),
                line=1,
                column=1,
            )
        ]
    )

def test_missing_closing_parenthesis_raises_parser_error():
    with pytest.raises(ParserError):
        parse_source("Result := (A + B;")