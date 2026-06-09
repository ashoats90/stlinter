from tokenizer import Tokenizer

source = """
VAR
    Motor_1 : BOOL;
    Count : INT;
END_VAR

(* Multi-line
   comment *)
IF Count >= 10 THEN
    Message := 'Count reached 10';
END_IF;
"""

for token in Tokenizer(source).tokenize():
    print(token)