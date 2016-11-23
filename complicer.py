FILE_EXAMPLE = 'example.ding'

TYPE_ID = 'ID'
TYPE_CONST_STRING = 'CONST_STRING'

TYPE_SY_LPAREN = 'LPAREN'
TYPE_SY_RPAREN = 'RPAREN'
TYPE_SY_LBRACE = 'LBRACE'
TYPE_SY_RBRACE = 'RBRACE'
TYPE_SY_SEMI = 'SEMI'
TYPE_SY_EOF = 'EOF'

TYPE_KW_DEF = 'def'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "Token: {type} {value}".format(
            type=self.type,
            value=repr(self.value)
        )


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


class Generator:
    def __init__(self, program):
        self.program = program

    def generate(self):
        result = ''
        result += 'public class ' + self.program.name + ' {\n\n'
        for fun in self.program.functions:
            result += '\tpublic static void ' + fun.name + '() {\n'
            for call in fun.block.statements:
                result += self.generate_statement(call)
            result += '\t}\n\n'
        result += '}'
        return result

    def generate_statement(self, call):
        result = ''
        result += '\t\t' + call.fun + '('
        if call.args:
            result += '"' + call.args[0].value + '"'
        result += ');\n'
        return result


def lexer_test():
    text = open(FILE_EXAMPLE, 'r').read()
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type is not TYPE_SY_EOF:
        print(token)
        token = lexer.get_next_token()


def parser_test():
    text = open(FILE_EXAMPLE, 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    program = parser.program('example')
    print(repr(program))


def generate_test():
    text = open(FILE_EXAMPLE, 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    program = parser.program('example')
    generator = Generator(program)
    print(generator.generate())


if __name__ == '__main__':
    generate_test()
