from _token import *


class AST:
    def __repr__(self):
        return repr(self.__dict__)


class Program(AST):
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions


class Function(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, statements):
        self.statements = statements


class Statement(AST):
    def __init__(self, operation, args):
        self.operation = operation
        self.args = args


class Call(AST):
    def __init__(self, fun, args):
        self.fun = fun
        self.args = args


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, type):
        if self.current_token.type is not type:
            self.error()
        else:
            self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def program(self, name):
        functions = []
        while self.current_token.type != TYPE_SY_EOF:
            functions.append(self.function())
        return Program(name, functions)

    def function(self):
        self.eat(TYPE_KW_DEF)
        name = self.current_token.value
        self.eat(TYPE_ID)
        self.eat(TYPE_SY_LPAREN)
        self.eat(TYPE_SY_RPAREN)
        block = self.block()
        return Function(name, block)

    def block(self):
        self.eat(TYPE_SY_LBRACE)
        statements = []
        while self.current_token.type != TYPE_SY_RBRACE:
            statements.append(self.statement())
        self.eat(TYPE_SY_RBRACE)
        return Block(statements)

    def statement(self):
        name = self.current_token.value
        self.eat(TYPE_ID)
        self.eat(TYPE_SY_LPAREN)
        args = []
        if self.current_token.type != TYPE_SY_RPAREN:
            args.append(self.current_token)
            self.current_token = self.lexer.get_next_token()
        self.eat(TYPE_SY_RPAREN)
        self.eat(TYPE_SY_SEMI)
        return Call(name, args)
