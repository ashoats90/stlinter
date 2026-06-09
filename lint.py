from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    IDENTIFIER = auto()
    KEYWORD = auto()
    NUMBER = auto()
    STRING = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    COMMENT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Tokenizer:

    def __init__(self, source: str):
        self.source = source
        self.i = 0
        self.line = 1
        self.column = 1

    def _peek(self) -> str:
        if self._at_end():
                return "\0"
        return self.source[self.i]

    def _advance(self) -> str:
         curr_char = self._peek()
         self.i += 1

         if curr_char == "\n":
              self.column = 1
              self.line += 1
         else:
              self.column += 1

         return curr_char
    
    def _advance_many(self, count) -> None:
         for _ in range(count):
              self._advance()
              
    def _at_end(self) -> bool:
        return (self.i >= len(self.source))
    
    def _starts_with(self, text: str) -> bool:
         return self.source.startswith(text, self.i)
         
    def _make_token(self, token_type: TokenType, value: str) -> Token:
         return Token(token_type, value, self.line, self.column)
    
    def _identifier_or_keyword(self) -> Token:
         start_i = self.i
         start_line = self.line
         start_col = self.column

         while not self._at_end() and (
              self._peek().isalnum() or self._peek() == "_"
         ):
              self._advance()
              
         value = self.source[start_i:self.i]
         
         if value.upper() in KEYWORDS:
              return Token(TokenType.KEYWORD, value.upper(), start_line, start_col)
         
         return Token(TokenType.IDENTIFIER, value, start_line, start_col)
    
    def _number(self) -> Token:
         start_i = self.i
         start_line = self.line
         start_col = self.column

         while not self._at_end() and self._peek().isdigit():
              self._advance()

         if not self._at_end() and self._peek() == ".":
              self._advance()

              while not self._at_end() and self._peek().isdigit():
                   self._advance()

         value = self.source[start_i:self.i]

         return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def _string(self) -> Token:
         start_i = self.i
         start_line = self.line
         start_col = self.column

         self._advance() # opening quote

         while not self._at_end() and self._peek() != "'":
              self._advance()

         if self._at_end():
              raise TokenizerError(
                   f"Unterminated string at line {start_line}, column {start_col}"
              )
         
         self._advance() # closing quote

         value = self.source[start_i:self.i]

         return Token(TokenType.STRING, value, start_line, start_col)
    
    def _line_comment(self) -> Token:
         start_i = self.i
         start_line = self.line
         start_col = self.column

         while not self._at_end() and self._peek() != "\n":
              self._advance()

         value = self.source[start_i:self.i]
         return Token(TokenType.COMMENT, value, start_line, start_col)

    def _block_comment(self) -> Token:
         start_i = self.i
         start_line = self.line
         start_col = self.column

         self._advance_many(2) # opening (*

         while not self._at_end() and not self._starts_with("*)"):
              self._advance()

         if self._at_end():
              raise TokenizerError(
                   f"Unterminated block comment at line {start_line}, column {start_col}"
              )
         
         self._advance_many(2) # closing *)

         value = self.source[start_i:self.i]

         return Token(TokenType.COMMENT, value, start_line, start_col)
    
    def _operator(self) -> Token:
         operator = self._match_multi_char_operator()

         if operator is not None:
              token = self._make_token(TokenType.OPERATOR, operator)
              self._advance_many(len(operator))
              return token
         
         character = self._peek()

         if character in SINGLE_CHAR_OPERATORS:
              token = self._make_token(TokenType.OPERATOR, character)
              self._advance()
              return token
         
         raise TokenizerError(
              f"Expected operator at line {self.line}, column {self.column}"
         )
    
    def _symbol(self) -> Token:
         symbol = self._peek()

         if symbol in SYMBOLS:
              token = self._make_token(TokenType.SYMBOL, symbol)
              self._advance()
              return token
         
         raise TokenizerError(
              f"Expected symbol at line {self.line}, column {self.column}"
         )
    
    def _match_multi_char_operator(self) -> str | None:
         for operator in sorted(MULTI_CHAR_OPERATORS, key=len, reverse=True):
              if self._starts_with(operator):
                   return operator
         return None
    
    def tokenize(self) -> list[Token]:
         
         tokens: list[Token] = []

         while not self._at_end():
              current_char = self._peek()

              if current_char in WHITESPACE:
                   self._advance()
                   continue
              
              elif self._starts_with("//"):
                   tokens.append(self._line_comment())
                   continue
              
              elif self._starts_with("(*"):
                   tokens.append(self._block_comment())
                   continue
              
              elif current_char == "'":
                   tokens.append(self._string())
                   continue

              if current_char.isalpha() or current_char == "_":
                   tokens.append(self._identifier_or_keyword())
                   continue

              elif current_char.isdigit():
                   tokens.append(self._number())
                   continue

              elif self._match_multi_char_operator() is not None or current_char in SINGLE_CHAR_OPERATORS:
                   tokens.append(self._operator())
                   continue
              
              elif current_char in SYMBOLS:
                   tokens.append(self._symbol())
                   continue

              else:
                   raise TokenizerError(
                        f"Unexpected character {current_char!r} at line {self.line}, column {self.column}"
                   )
              
         tokens.append(Token(TokenType.EOF, "", self.line, self.column))

         return tokens
    
class TokenizerError(Exception):
     pass

KEYWORDS = set([
    "VAR",
    "END_VAR",
    "IF",
    "THEN",
    "ELSE",
    "ELSIF",
    "END_IF",
    "TRUE",
    "FALSE",
])

MULTI_CHAR_OPERATORS = set([
    ":=",
    "<=",
    ">=",
    "<>",
])

SYMBOLS = set([
    ";",
    ",",
    "(",
    ")",
    ".",
])

SINGLE_CHAR_OPERATORS = set([
    "+",
    "-",
    "*",
    "/",
    "=",
    "<",
    ">",
    ":",
])

WHITESPACE = set([
     " ",
     "\t",
     "\r",
     "\n",
])

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