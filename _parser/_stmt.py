from _parser._expr import *

ASSIGN_OP_LIST = [SY_EQUAL, SY_ADD_ASSIGN, SY_MINUS_ASSIGN, SY_MOD_ASSIGN,
                  SY_MUL_ASSIGN, SY_ADD_ASSIGN, SY_OR_ASSIGN, SY_XOR_ASSIGN,
                  SY_DIV_ASSIGN]

BLOCK_TYPE_STMT = 0x01
BLOCK_TYPE_FUNCTION = 0x02
BLOCK_TYPE_CLASS = 0x03


class Stmt(AST):
    def __init__(self, assignop, left, right):
        self.assignop = assignop
        self.left = left
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.assignop + repr(self.right) + ';'


class Variable(AST):
    def __init__(self, name, clazz, block):
        self.name = name
        self.clazz = clazz
        self.block = block

    def __repr__(self):
        return '(Var ' + self.name + ':' + repr(self.clazz) + ')'


class Block(AST):
    def __init__(self, parent, stmts, type=BLOCK_TYPE_STMT):
        self.parent = parent
        self.stmts = stmts
        self.vars = {}
        self.type = type

    def add_var(self, name, clazz):
        self.vars[name] = Variable(name, clazz, self)

    def contains(self, name):
        return name in self.vars.keys()

    def get_var(self, name):
        return self.vars[name]

    def __repr__(self):
        ret = '{\n'
        for stmt in self.stmts:
            ret += repr(stmt)
            ret += '\n'
        ret += '}\n[\n'
        for var in self.vars.values():
            ret += repr(var)
            ret += '\n'
        ret += ']'
        return ret


class IF(AST):
    def __init__(self, expr, stmt, else_stmt=None):
        self.expr = expr
        self.stmt = stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        ret = 'if (' + repr(self.expr) + ') { ' + repr(self.stmt)
        if self.else_stmt:
            ret += '} else {' + repr(self.else_stmt)
        ret += '}'
        return ret


class WHILE(AST):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def __repr__(self):
        return 'while (' + repr(self.expr) + ') { ' + repr(self.stmt) + ' }'


class DO(WHILE):
    def __repr__(self):
        return 'do { ' + repr(self.stmt) + ' }' + ' while(' + repr(self.expr) + ')'


class Declaration(Stmt):
    def __init__(self, type, name, right=None):
        if right:
            Stmt.__init__(self, SY_ASSIGN, (type, name), right)
        else:
            Stmt.__init__(self, None, (type, name), None)

    def __repr__(self):
        if self.assignop:
            return "Define:" + Stmt.__repr__(self)
        else:
            return "Declaration:" + repr(self.left[0]) + self.left[1]


class StmtParser(ExprParser):
    def block(self, parent):
        block = Block(parent, [])
        self.eat_sy(SY_LBRACE)
        stmts = self.stmts(block)
        self.eat_sy(SY_RBRACE)
        block.stmts = stmts
        return block

    def stmts(self, block):
        ret = []
        while not self.current_token.match_category(CATEGORY_SY_EOF) and self.current_token.value is not SY_RBRACE:
            stmt = self.stmt(block)
            ret.append(stmt)
        return ret

    def stmt(self, block):
        if self.is_type(self.current_token):
            type = self.current_token
            self.eat_type()
            name = self.current_token.value
            self.eat_id()
            block.add_var(name, type)
            if self.current_token.value == SY_ASSIGN:
                self.eat_sy(SY_ASSIGN)
                right = self.expr()
                self.eat_semi()
                return Declaration(type, name, right)
            self.eat_semi()
            return Declaration(type, name)
        if self.current_token.match_category(CATEGORY_KW_STMT):
            return self.kw_stmt(block)
        expr = self.expr()
        if self.current_token.value is SY_SEMI:
            self.eat_semi()
            return expr
        if self.current_token.match_category(CATEGORY_SY_ASSIGN):
            op = self.current_token.value
            self.eat_sy()
            right = self.expr()
            self.eat_semi()
            return Stmt(op, expr, right)

    def kw_stmt(self, block):
        value = self.current_token.value
        if value is KW_IF:
            return self.if_stmt(block)
        if value is KW_DO:
            return self.do_stmt(block)
        if value is KW_WHILE:
            return self.while_stmt(block)
        self.error('not support kw: ' + repr(self.current_token))

    def variable(self):
        # todo 添加定义变量
        return ExprParser.variable(self)

    def is_type(self, token):
        return token.match_category(CATEGORY_KW_BT)

    def eat_type(self):
        self.eat_kw(category=CATEGORY_KW_BT)

    def eat_semi(self):
        self.eat_sy(SY_SEMI)

    def if_stmt(self, block):
        self.eat_kw(KW_IF)
        self.eat_sy(SY_LPAREN)
        expr = self.expr()
        self.eat_sy(SY_RPAREN)
        stmt = self.stmt(block)
        if self.current_token.value is KW_ELSE:
            self.eat_kw(KW_ELSE)
            else_stmt = self.stmt(block)
            return IF(expr, stmt, else_stmt)
        return IF(expr, stmt)

    def do_stmt(self, block):
        self.eat_kw(KW_DO)
        stmt = self.stmt(block)
        self.eat_kw(KW_WHILE)
        self.eat_sy(SY_LPAREN)
        expr = self.expr()
        self.eat_sy(SY_RPAREN)
        return DO(expr, stmt)

    def while_stmt(self, block):
        self.eat_kw(KW_WHILE)
        self.eat_sy(SY_LPAREN)
        expr = self.expr()
        self.eat_sy(SY_RPAREN)
        stmt = self.stmt(block)
        return WHILE(expr, stmt)


if __name__ == '__main__':
    from _lexer import Lexer

    stmts = ''' {
    a[3/5] = 10 + 2 / 3 * a;
    int b = 3;
    float c = 2.6;
    string str = "strre"+"cds";
    if (2+9/6) str = "dfds";
    if (3) c = 3.2; else c = 3.6;
    do ++b; while(b > 5)
    while(b >=0) a[4/7] = 68+928;
    } '''
    lexer = Lexer(stmts)
    parser = StmtParser(lexer)
    ret = parser.block(None)
    print(stmts)
    print(ret)
