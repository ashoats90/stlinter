from stlinter.tokens import Token, TokenType
from stlinter.ast_nodes import Program, VarDecl, Assignment, BooleanLiteral, StringLiteral, NumberLiteral, Identifier, IfStatement, BinaryExpression

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
    
    def parse(self) -> Program:
        statements = []

        while not self._at_end():
            if self._check(TokenType.KEYWORD, "VAR"):
                statements.extend(self._parse_var_block())
            elif self._check(TokenType.IDENTIFIER):
                statements.append(self._parse_assignment())
            elif self._check(TokenType.KEYWORD, "IF"):
                statements.append(self._parse_if_statement())
            else:
                current_token = self._peek()
                raise ParserError(
                    f'Unexpected token {current_token.type.name}("{current_token.value}") '
                    f"at line {current_token.line}, column {current_token.column}"
                )
            
        return Program(statements)
    
    def _parse_var_block(self) -> list[VarDecl]:
        declarations = []

        self._expect(TokenType.KEYWORD, "VAR")

        while not self._check(TokenType.KEYWORD, "END_VAR"):
            declarations.append(self._parse_var_decl())

        self._expect(TokenType.KEYWORD, "END_VAR")

        return declarations
    
    def _parse_var_decl(self) -> VarDecl:
        name_token = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.OPERATOR, ":")
        type_token = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.SYMBOL, ";")

        return VarDecl(
            name_token.value,
            type_token.value,
            name_token.line,
            name_token.column,
        )
    
    def _parse_assignment(self) -> Assignment:
        target_token = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.OPERATOR, ":=")
        value = self._parse_expression()
        self._expect(TokenType.SYMBOL, ";")

        return Assignment(
            target=target_token.value,
            value=value,
            line=target_token.line,
            column=target_token.column,
        )

    def _parse_primary(self) -> object:
        if self._check(TokenType.KEYWORD, "TRUE"):
            token = self._expect(TokenType.KEYWORD, "TRUE")
            return BooleanLiteral(True, token.line, token.column)
        elif self._check(TokenType.KEYWORD, "FALSE"):
            token = self._expect(TokenType.KEYWORD, "FALSE")
            return BooleanLiteral(False, token.line, token.column)
        elif self._check(TokenType.STRING):
            token = self._expect(TokenType.STRING)
            return StringLiteral(token.value[1:-1], token.line, token.column)
        elif self._check(TokenType.NUMBER):
            token = self._expect(TokenType.NUMBER)
            return NumberLiteral(token.value, token.line, token.column)
        elif self._check(TokenType.IDENTIFIER):
            token = self._expect(TokenType.IDENTIFIER)
            return Identifier(token.value, token.line, token.column)
        
        current_token = self._peek()

        raise ParserError(
            f'Unexpected token {current_token.type.name}("{current_token.value}") '
            f"at line {current_token.line}, column {current_token.column}"
        )
    
    def _parse_expression(self) -> object:
        left = self._parse_primary()

        if self._check(TokenType.OPERATOR) and self._peek().value in BINARY_OPERATORS:
            operator_token = self._advance()
            right = self._parse_primary()

            return BinaryExpression(
                left=left,
                operator=operator_token.value,
                right=right,
                line=left.line,
                column=left.column,
            )
        
        return left
    
    def _parse_statement(self) -> object:
        if self._check(TokenType.KEYWORD, "IF"):
            return self._parse_if_statement()
        
        if self._check(TokenType.IDENTIFIER):
            return self._parse_assignment()
        
        current_token = self._peek()
        raise ParserError(
            f'Unexpected token {current_token.type.name}("{current_token.value}") '
            f"at line {current_token.line}, column {current_token.column}"
        )
    
    def _parse_if_statement(self) -> IfStatement:
        if_token = self._expect(TokenType.KEYWORD, "IF")
        condition = self._parse_expression()
        self._expect(TokenType.KEYWORD, "THEN")

        body = []

        while not self._check(TokenType.KEYWORD, "END_IF"):
            body.append(self._parse_statement())

        self._expect(TokenType.KEYWORD, "END_IF")
        self._expect(TokenType.SYMBOL, ";")

        return IfStatement(
            condition=condition,
            body=body,
            line=if_token.line,
            column=if_token.column,
        )
    
BINARY_OPERATORS = {"+", "-", "*", "/", "=", "<>", "<", ">", "<=", ">="}