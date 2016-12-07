from _parser._stmt import *


class Clazz(AST):
    def __init__(self, name, methods, block):
        self.name = name
        self.methods = methods
        self.block = block

    def __repr__(self):
        ret = 'class ' + self.name + '['
        for method in self.methods:
            ret += repr(method) + ' '
        ret += ']\n' + repr(self.block)
        return ret


class Function(AST):
    def __init__(self, name, arglist, block):
        self.name = name
        self.arglist = arglist
        self.block = block

    def __repr__(self):
        ret = 'def ' + self.name + '('
        for type,name in self.arglist:
            ret += repr(type) + ' ' + name + ','
        ret = ret[:-1]
        ret += ')' + repr(self.block)
        return ret


class ClassParser(StmtParser):
    def clazz(self, parent):
        self.eat_kw(KW_CLASS)
        name = self.current_token.value
        parent.add_class(name, parent.package)
        self.eat_id()
        self.eat_sy(SY_LBRACE)
        methods = []
        block = Block(parent, parent.package + '.' + name, BLOCK_TYPE_CLASS)
        while self.current_token.value is not SY_RBRACE:
            if self.current_token.value is KW_DEF:
                method = self.function(block)
                methods.append(method.name)
                block.add_stmt(method)
                continue
            self.error('class synax error')
        self.eat_sy(SY_RBRACE)
        return Clazz(name, methods, block)

    def function(self, parent):
        self.eat(KW_DEF)
        name = self.current_token.value
        parent.add_function(name)
        self.eat_id()
        self.eat(SY_LPAREN)
        if self.current_token.value != SY_RPAREN:
            arglist = self.arglist(parent)
        else:
            arglist = []
        self.eat(SY_RPAREN)
        block = self.block(parent, parent.package, arglist)
        return Function(name, arglist, block)

    def arglist(self, block):
        ret = []
        type = self.current_token
        name = ''
        if self.is_type(self.current_token, block):
            self.eat_type()
            name = self.current_token.value
            self.eat_id()
        else:
            self.error('argument synatx error')
        while self.current_token.value != SY_RPAREN:
            ret.append((type, name))
            self.eat(SY_COMMA)
            type = self.current_token
            if self.is_type(self.current_token, block):
                self.eat_type()
                name = self.current_token.value
                self.eat_id()
            else:
                self.error('argument synatx error')
        ret.append((type, name))
        return ret


if __name__ == '__main__':
    from _lexer import Lexer

    text = open('class.ding', 'r').read()
    lexer = Lexer(text)
    parser = ClassParser(lexer)
    ret = parser.clazz(Block(None, '', BLOCK_TYPE_FILE))
    print(text)
    print(ret)
