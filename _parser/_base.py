from _global import *


class AST:
    def __repr__(self):
        return '\n' + str(self.__class__) + '\n' + repr(self.__dict__)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, value=None, type=None, category=CATEGORY_NONE):
        if value and self.current_token.value is not value:
            self.error()
        if type and self.current_token.type is not type:
            self.error()
        if category is not CATEGORY_NONE and not self.current_token.match_category(category):
            self.error()
        self.next_token()

    def eat_id(self, id=None, category=CATEGORY_NONE):
        self.eat(value=id, type=TYPE_ID, category=category)

    def eat_sy(self, symbol=None, category=CATEGORY_NONE):
        self.eat(value=symbol, type=TYPE_SYMBOL, category=category)

    def eat_kw(self, key=None, category=CATEGORY_NONE):
        self.eat(value=key, type=TYPE_KEYWORD, category=category)

    def error(self, msg=None):
        text = 'Invalid syntax'
        if msg:
            text += ': ' + msg
        else:
            text += repr(self.current_token)
        raise Exception(text)

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
