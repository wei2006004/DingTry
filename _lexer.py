from _global import *


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
            if self.current_char in SY_LIST:
                char = self.current_char
                self.advance()
                return SY_MAP[char]
            self.error()
        return SY_MAP[SY_EOF]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result in KW_LIST:
            return KW_MAP[result]
        if result in BT_LIST:
            return BT_MAP[result]
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


if __name__ == '__main__':
    text = open('example.ding', 'r').read()
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.value is not SY_EOF:
        print(token)
        token = lexer.get_next_token()