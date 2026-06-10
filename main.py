from stlinter.tokenizer import Tokenizer
from stlinter.parser import Parser

source = """
VAR
    MotorRun : BOOL;
    Count : INT;
END_VAR
"""

tokens = Tokenizer(source).tokenize()
program = Parser(tokens).parse()

print(program)