from _global import *


class AST:
    def __repr__(self):
        return '\n' + str(self.__class__) + '\n' + repr(self.__dict__)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, value=None, type=None):
        if value is None:
            self.current_token = self.lexer.get_next_token()
        elif self.current_token.value is not value:
            self.error()
        else:
            if type and self.current_token.value is not type:
                self.error()
            else:
                self.current_token = self.lexer.get_next_token()

    def eat_id(self, id=None):
        self.eat(value=id, type=TYPE_ID)

    def eat_bt(self, type=None):
        self.eat(value=type, type=TYPE_BUILDIN_TYPE)

    def eat_kw(self, key=None):
        self.eat(value=key, type=TYPE_KEYWORD)

    def error(self):
        raise Exception('Invalid syntax')