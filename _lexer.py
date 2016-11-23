from _token import *


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == '"':
                return self.string()
            if self.current_char == ';':
                self.advance()
                return Token(TYPE_SY_SEMI, ';')
            if self.current_char == '{':
                self.advance()
                return Token(TYPE_SY_LBRACE, '{')
            if self.current_char == '}':
                self.advance()
                return Token(TYPE_SY_RBRACE, '}')
            if self.current_char == '(':
                self.advance()
                return Token(TYPE_SY_LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(TYPE_SY_RPAREN, ')')
            self.error()
        return Token(TYPE_SY_EOF, None)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result == TYPE_KW_DEF:
            return Token(TYPE_KW_DEF, TYPE_KW_DEF)
        return Token(TYPE_ID, result)

    def error(self):
        raise Exception('Invalid character')

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char is not '"':
            result += self.current_char
            self.advance()
        self.advance()
        return Token(TYPE_CONST_STRING, result)
