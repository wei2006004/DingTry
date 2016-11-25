from _global import *


class AST:
    def __repr__(self):
        return '\n' + str(self.__class__) + '\n' + repr(self.__dict__)


class Program(AST):
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions


class Function(AST):
    def __init__(self, name, arglist, block):
        self.name = name
        self.arglist = arglist
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

    def eat(self, value):
        if self.current_token.value is not value:
            self.error()
        else:
            self.current_token = self.lexer.get_next_token()

    def eat_id(self):
        if self.current_token.type is not TYPE_ID:
            self.error()
        else:
            self.current_token = self.lexer.get_next_token()

    def eat_bt(self):
        if self.current_token.type is not TYPE_BUILDIN_TYPE:
            self.error()
        else:
            self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def program(self, name):
        functions = []
        while self.current_token.value != SY_EOF:
            functions.append(self.function())
        return Program(name, functions)

    def function(self):
        self.eat(KW_DEF)
        name = self.current_token.value
        self.eat_id()
        self.eat(SY_LPAREN)
        if self.current_token.value != SY_RPAREN:
            arglist = self.arglist()
        else:
            arglist = None
        self.eat(SY_RPAREN)
        block = self.block()
        return Function(name, arglist, block)

    def block(self):
        self.eat(SY_LBRACE)
        statements = []
        while self.current_token.value != SY_RBRACE:
            statements.append(self.statement())
        self.eat(SY_RBRACE)
        return Block(statements)

    def statement(self):
        name = self.current_token.value
        self.eat_id()
        self.eat(SY_LPAREN)
        args = []
        if self.current_token.value != SY_RPAREN:
            args.append(self.current_token)
            self.current_token = self.lexer.get_next_token()
        self.eat(SY_RPAREN)
        self.eat(SY_SEMI)
        return Call(name, args)

    def arglist(self):
        ret = []
        type = self.current_token.value
        self.eat_bt()
        name = self.current_token.value
        self.eat_id()
        while self.current_token.value != SY_RPAREN:
            ret.append((type, name))
            self.eat(SY_COMMA)
            type = self.current_token.value
            self.eat_bt()
            name = self.current_token.value
            self.eat_id()
        ret.append((type, name))
        return ret


if __name__ == '__main__':
    text = open('example.ding', 'r').read()
    from _lexer import Lexer

    lexer = Lexer(text)
    parser = Parser(lexer)
    program = parser.program('example')
    print(repr(program))
