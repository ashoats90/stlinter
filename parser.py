from tokens import Token, TokenType
from ast_nodes import Program, VarDecl

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0

    def _peek(self) -> Token:
        return self.tokens[self.i]
    
    def _advance(self) -> Token:
        current_token = self._peek()

        if not self._at_end():
            self.i += 1

        return current_token
    
    def _at_end(self) -> bool:
        return self._peek().type == TokenType.EOF
    
    def _check(self, token_type: TokenType, value: str | None = None) -> bool:
        curr_token = self._peek()

        if value is not None:
            return curr_token.type == token_type and curr_token.value == value
        
        return curr_token.type == token_type
    
    def _expect(self, token_type: TokenType, value: str | None = None) -> Token:
        if self._check(token_type, value):
            return self._advance()
        
        current_token = self._peek()
        expected = token_type.name if value is None else f'{token_type.name}("{value}")'

        raise ParserError(
            f'Expected {expected}, found {current_token.type.name}("{current_token.value}") '
            f"at line {current_token.line}, column {current_token.column}"
        )
    
     