import pytest

from stlinter.tokenizer import Tokenizer, TokenizerError
from stlinter.tokens import TokenType


def test_tokenizes_simple_assignment():
    tokens = Tokenizer("MotorRun := TRUE;").tokenize()

    assert [(t.type, t.value) for t in tokens] == [
        (TokenType.IDENTIFIER, "MotorRun"),
        (TokenType.OPERATOR, ":="),
        (TokenType.KEYWORD, "TRUE"),
        (TokenType.SYMBOL, ";"),
        (TokenType.EOF, ""),
    ]


def test_tokenizes_var_block():
    source = """
VAR
    MotorRun : BOOL;
END_VAR
"""
    tokens = Tokenizer(source).tokenize()

    assert [(t.type, t.value) for t in tokens] == [
        (TokenType.KEYWORD, "VAR"),
        (TokenType.IDENTIFIER, "MotorRun"),
        (TokenType.OPERATOR, ":"),
        (TokenType.IDENTIFIER, "BOOL"),
        (TokenType.SYMBOL, ";"),
        (TokenType.KEYWORD, "END_VAR"),
        (TokenType.EOF, ""),
    ]


def test_tokenizes_comments():
    source = """
// line comment
(* block
   comment *)
"""
    tokens = Tokenizer(source).tokenize()

    assert [(t.type, t.value) for t in tokens] == [
        (TokenType.COMMENT, "// line comment"),
        (TokenType.COMMENT, "(* block\n   comment *)"),
        (TokenType.EOF, ""),
    ]


def test_unterminated_string_raises():
    with pytest.raises(TokenizerError):
        Tokenizer("'oops").tokenize()


def test_unterminated_block_comment_raises():
    with pytest.raises(TokenizerError):
        Tokenizer("(* oops").tokenize()