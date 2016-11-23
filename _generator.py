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
