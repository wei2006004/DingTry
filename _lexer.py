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

    def peek(self):
        peekpos = self.pos + 1
        if peekpos >= len(self.text):
            return None
        else:
            return self.text[peekpos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                return self._id()
            if self.current_char.isdigit():
                return self.number()
            if self.current_char == '"':
                return self.string()
            if self.current_char in SY_DOUBLE_HEAD_LIST and self.peek() is not None:
                sy = ''
                sy += self.current_char
                sy += self.peek()
                if sy in SY_DOUBLE_LIST:
                    self.advance()
                    self.advance()
                    return SY_MAP[sy]
            if self.current_char in SY_SINGLE_LIST:
                char = self.current_char
                self.advance()
                return SY_MAP[char]
            self.error(self.current_char)
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
        return Token(TYPE_ID, result)

    def error(self, char):
        raise Exception('Invalid character: ' + char)

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char is not '"':
            result += self.current_char
            self.advance()
        self.advance()
        return Token(TYPE_CONST_STRING, result)

    def number(self):
        ret = ''
        while self.current_char is not None and self.current_char.isdigit():
            ret += self.current_char
            self.advance()
        if self.current_char is '.':
            ret += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                ret += self.current_char
                self.advance()
            token = Token(TYPE_CONST_FLOAT, float(ret))
        else:
            token = Token(TYPE_CONST_INT, int(ret))
        return token


if __name__ == '__main__':
    text = '>=+= <> 12 string fad def == + ='
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.value is not SY_EOF:
        print(token)
        token = lexer.get_next_token()