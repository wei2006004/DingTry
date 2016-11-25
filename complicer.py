from _global import SY_EOF
from _lexer import Lexer
from _parser import Parser
from _generator import Generator

FILE_EXAMPLE = 'example.ding'


def lexer_test():
    text = open(FILE_EXAMPLE, 'r').read()
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type is not SY_EOF:
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
