FUN_PRINTIN = 'println'


class Generator:
    def __init__(self, program):
        self.program = program

    def generate(self):
        result = ''
        result += 'public class ' + self.program.name + ' {\n\n'
        for fun in self.program.functions:
            result += '\tpublic static void ' + fun.name + '('
            result += self.gen_arglist(fun)
            result += ') {\n'
            for call in fun.block.statements:
                result += self.generate_statement(call)
            result += '\t}\n\n'
        result += '}'
        return result

    def gen_arglist(self, fun):
        args = fun.arglist
        ret = ''
        for type, name in args:
            ret += type + ' ' + name + ','
        ret = ret[:-1]
        return ret

    def generate_statement(self, call):
        result = ''
        name = call.fun
        if call.fun == FUN_PRINTIN:
            name = 'System.out.println'
        result += '\t\t' + name + '('
        if call.args:
            result += '"' + call.args[0].value + '"'
        result += ');\n'
        return result


if __name__ == '__main__':
    from _lexer import Lexer
    from _parser import Parser
    text = open('example.ding', 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    program = parser.program('example')
    generator = Generator(program)
    print(generator.generate())
