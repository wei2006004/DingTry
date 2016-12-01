from _global import *


class AST:
    def __repr__(self):
        return '\n' + str(self.__class__) + '\n' + repr(self.__dict__)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, value=None, type=None):
        if value and self.current_token.value is not value:
            self.error()
        if type and self.current_token.type is not type:
            self.error()
        self.next_token()

    def eat_id(self, id=None):
        self.eat(value=id, type=TYPE_ID)

    def eat_sy(self, symbol=None):
        self.eat(value=symbol, type=TYPE_SYMBOL)

    def eat_kw(self, key=None):
        self.eat(value=key, type=TYPE_KEYWORD)

    def error(self, msg=None):
        text = 'Invalid syntax'
        if msg:
            text += ': ' + msg
        else:
            text += repr(self.current_token)
        raise Exception(text)

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
