from _parser._expr import *


class Stmt(AST):
    def __init__(self, assignop, left, right):
        self.assignop = assignop
        self.left = left
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.assignop + repr(self.right) + ';'


class Kw_Stmt(AST):
    def __init__(self, keyword, expr, stmt, block):
        if stmt is None and block is None:
            raise SyntaxError('kw stmt has no stmt:' + keyword)
        self.keyword = keyword
        self.expr = expr
        self.stmt = stmt
        self.block = block

    def __repr__(self):
        ret = self.keyword
        if self.expr:
            ret += ' (' + repr(self.expr) + ') '
        if self.block:
            ret += repr(self.block)
        else:
            ret += repr(self.stmt)
        return ret


class WHILE(Kw_Stmt):
    def __init__(self, expr, stmt, block):
        Kw_Stmt.__init__(self, 'while', expr, stmt, block)


class ELSE(Kw_Stmt):
    def __init__(self, stmt, block):
        Kw_Stmt.__init__(self, 'else', None, stmt, block)


class IF(Kw_Stmt):
    def __init__(self, expr, stmt, block, other_stmt=None):
        Kw_Stmt.__init__(self, 'if', expr, stmt, block)
        self.other_stmt = other_stmt

    def __repr__(self):
        ret = Kw_Stmt.__repr__(self)
        if self.other_stmt:
            ret += repr(self.other_stmt)
        return ret


class ELIF(IF):
    def __init__(self, expr, stmt, block, other_stmt=None):
        IF.__init__(self, expr, stmt, block, other_stmt)
        self.keyword = 'elif'


class DO(Kw_Stmt):
    def __init__(self, expr, stmt, block):
        Kw_Stmt.__init__(self, 'do', expr, stmt, block)

    def __repr__(self):
        ret = 'do '
        if self.block:
            ret += repr(self.block)
        else:
            ret += repr(self.stmt)
        ret += 'while(' + repr(self.expr) + ')'
        return ret


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
    def block(self, parent, package, arglist=[]):
        block = Block(parent, [], package)
        for type, name in arglist:
            block.add_var(name, type, VAR_TYPE_ARGUMENT)
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
        if self.is_type(self.current_token, block):
            type = self.current_token
            self.eat_type()
            name = self.current_token.value
            self.eat_id()
            block.add_local_var(name, type)
            if self.current_token.value == SY_ASSIGN:
                self.eat_sy(SY_ASSIGN)
                right = self.expr(block)
                self.eat_semi()
                return Declaration(type, name, right)
            self.eat_semi()
            return Declaration(type, name)
        if self.current_token.match_category(CATEGORY_KW_STMT):
            return self.kw_stmt(block)
        expr = self.expr(block)
        if self.current_token.value is SY_SEMI:
            self.eat_semi()
            return expr
        if self.current_token.match_category(CATEGORY_SY_ASSIGN):
            op = self.current_token.value
            self.eat_sy()
            right = self.expr(block)
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

    def is_type(self, token, block):
        if token.match_category(CATEGORY_KW_BT):
            return True
        return block.get_class_recur(token.value, block.package) is not None

    def eat_type(self, is_bt=True):
        if is_bt:
            self.eat_kw(category=CATEGORY_KW_BT)
        else:
            self.eat_id()

    def eat_semi(self):
        self.eat_sy(SY_SEMI)

    def if_stmt(self, parent):
        self.eat_kw(KW_IF)
        expr = self.bool_expr(parent)
        stmt, block = self.stmt_or_block(parent)
        if self.current_token.value is KW_ELIF:
            other_stmt = self.elif_stmt(parent)
            return IF(expr, stmt, block, other_stmt)
        if self.current_token.value is KW_ELSE:
            other_stmt = self.else_stmt(parent)
            return IF(expr, stmt, block, other_stmt)
        return IF(expr, stmt, block)

    def do_stmt(self, parent):
        self.eat_kw(KW_DO)
        stmt, block = self.stmt_or_block(parent)
        self.eat_kw(KW_WHILE)
        expr = self.bool_expr(parent)
        return DO(expr, stmt, block)

    def while_stmt(self, parent):
        self.eat_kw(KW_WHILE)
        expr = self.bool_expr(parent)
        stmt, block = self.stmt_or_block(parent)
        return WHILE(expr, stmt, block)

    def elif_stmt(self, parent):
        self.eat_kw(KW_ELIF)
        expr = self.bool_expr(parent)
        stmt, block = self.stmt_or_block(parent)
        if self.current_token.value is KW_ELIF:
            other_stmt = self.elif_stmt(parent)
            return ELIF(expr, stmt, block, other_stmt)
        if self.current_token.value is KW_ELSE:
            other_stmt = self.else_stmt(parent)
            return ELIF(expr, stmt, block, other_stmt)
        return ELIF(expr, stmt, block)

    def else_stmt(self, parent):
        self.eat_kw(KW_ELSE)
        stmt, block = self.stmt_or_block(parent)
        return ELSE(stmt, block)

    def stmt_or_block(self, parent):
        block = None
        stmt = None
        if self.current_token.value is SY_LBRACE:
            block = self.block(parent, parent.package)
        else:
            stmt = self.stmt(parent)
        return stmt, block

    def bool_expr(self, block):
        self.eat_sy(SY_LPAREN)
        expr = self.expr(block)
        self.eat_sy(SY_RPAREN)
        return expr


if __name__ == '__main__':
    from _lexer import Lexer

    stmts = open('stmt.ding', 'r').read()
    lexer = Lexer(stmts)
    parser = StmtParser(lexer)
    ret = parser.block(None, '')
    print(stmts)
    print(ret)
