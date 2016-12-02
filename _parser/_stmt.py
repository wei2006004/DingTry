from _parser._expr import *

ASSIGN_OP_LIST = [SY_EQUAL, SY_ADD_ASSIGN, SY_MINUS_ASSIGN, SY_MOD_ASSIGN,
                  SY_MUL_ASSIGN, SY_ADD_ASSIGN, SY_OR_ASSIGN, SY_XOR_ASSIGN,
                  SY_DIV_ASSIGN]


class Stmt(AST):
    def __init__(self, assignop, left, right):
        self.assignop = assignop
        self.left = left
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.assignop + repr(self.right) + ';'


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
    def stmts(self):
        ret = []
        while not self.current_token.match_category(CATEGORY_SY_EOF) and self.current_token.value is not SY_RBRACE:
            stmt = self.stmt()
            ret.append(stmt)
        return ret

    def stmt(self):
        if self.is_type(self.current_token):
            type = self.current_token
            self.eat_type()
            name = self.variable()
            if self.current_token.value == SY_ASSIGN:
                self.eat_sy(SY_ASSIGN)
                right = self.expr()
                self.eat_semi()
                return Declaration(type, name, right)
            self.eat_semi()
            return Declaration(type, name)
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

    def variable(self):
        return ExprParser.variable(self)

    def is_type(self, token):
        return token.match_category(CATEGORY_KW_BT)

    def eat_type(self):
        self.eat_kw(category=CATEGORY_KW_BT)

    def eat_semi(self):
        self.eat_sy(SY_SEMI)


if __name__ == '__main__':
    from _lexer import Lexer

    stmts = '''
    a[3/5] = 10 + 2 / 3 * a;
    int b = 3;
    float c = 2.6;
    string str = "strre"+"cds";
    '''
    lexer = Lexer(stmts)
    parser = StmtParser(lexer)
    ret = parser.stmts()
    print(stmts)
    for stmt in ret:
        print(stmt)
