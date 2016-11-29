from _parser._base import *

# 双目运算符，从左到右，优先级从高到低
BINOP_LIST = [[SY_MUL, SY_DIV, SY_MOD],
              [SY_PLUS, SY_MINUS],
              [SY_LSHIFT, SY_RSHIFT],
              [SY_GREATER, SY_GREATER_EQUAL, SY_LESS, SY_LESS_EQUAL],
              [SY_EQUAL, SY_NOT_EQUAL],
              [SY_AND],
              [SY_XOR],
              [SY_OR],
              [SY_LOG_AND],
              [SY_LOG_OR]]

# 单目运算符，从右到左
UNIOP_LIST = [SY_PLUS, SY_MINUS, SY_INC, SY_DEC, SY_NOT, SY_LOG_NOT]


class UniOp(AST):
    def __init__(self, operation, value):
        self.operation = operation
        self.value = value

    def __repr__(self):
        return '(' + self.operation + repr(self.value) + ')'


class BinOp(AST):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        return '(' + repr(self.left) + self.operation + repr(self.right) + ')'


class TriOp(AST):
    def __init__(self, operation, left, middle, right):
        self.operation = operation
        self.left = left
        self.middle = middle
        self.right = right

    def __repr__(self):
        return '(' + self.operation + ': ' + repr(self.left) + ', ' + repr(self.middle) + ', ' + repr(self.right) + ')'


class Call(AST):
    def __init__(self, var, arglist):
        self.var = var
        self.arglist = arglist

    def __repr__(self):
        return repr(self.var) + '(' + ','.join([repr(arg) for arg in self.arglist]) + ')'


class Offset(AST):
    def __init__(self, var, index):
        self.var = var
        self.index = index

    def __repr__(self):
        return repr(self.var) + '[' + repr(self.index) + ']'


class ExprParser(Parser):
    def factor(self):
        if self.current_token.type in [TYPE_CONST_INT, TYPE_CONST_STRING, TYPE_CONST_FLOAT]:
            token = self.current_token
            self.eat(type=self.current_token.type)
            return token.value
        if self.current_token.value is SY_LPAREN:
            self.eat_sy(SY_LPAREN)
            expr = self.expr()
            self.eat_sy(SY_RPAREN)
            return expr
        var = self.variable()
        if self.current_token.value is SY_LPAREN:
            self.eat_sy(SY_LPAREN)
            arglist = []
            while self.current_token.value is not SY_RPAREN:
                arglist.append(self.expr())
                if self.current_token.value is not SY_RPAREN:
                    self.eat_sy(SY_COMMA)
            self.eat_sy(SY_RPAREN)
            return Call(var, arglist)
        if self.current_token.value is SY_LBRACKET:
            self.eat_sy(SY_LBRACKET)
            index = self.expr()
            self.eat_sy(SY_RBRACKET)
            return Offset(var, index)
        self.error('no match factor:' + repr(self.current_token))

    def expr(self):
        return self.triop()

    def triop(self):
        left = self.binop()
        if self.current_token.value is SY_QUEST:
            self.eat_sy()
            middle = self.triop()
            self.eat_sy(SY_COLON)
            right = self.triop()
            return TriOp(SY_QUEST, left, middle, right)
        return left

    def binop(self, index=len(BINOP_LIST)):
        if index == 0:
            return self.uniop()
        tree = self.binop(index - 1)
        while self.current_token.value is not SY_EOF and self.current_token.value in BINOP_LIST[index - 1]:
            operation = self.current_token.value
            self.eat_binop(index - 1)
            right = self.binop(index - 1)
            if right is None:
                self.error('right is empty:' + operation)
            tree = BinOp(operation, tree, right)
        return tree

    def eat_binop(self, index):
        if self.current_token.value not in BINOP_LIST[index]:
            self.error('index:' + index + ' value:' + self.current_token.value)
        self.eat_sy()

    def uniop(self):
        if self.current_token.value in UNIOP_LIST:
            operation = self.current_token.value
            self.eat_sy()
            value = self.uniop()
            return UniOp(operation, value)
        return self.factor()

    def variable(self):
        var = self.current_token.value
        self.eat_id()
        return var


if __name__ == '__main__':
    print(BINOP_LIST)
    print(UNIOP_LIST)
    from _lexer import Lexer

    expr = '2+abc[2+4/5]-3 ? c(4|6,9,"as")-"sdc"*6.67|-1 : 6 && (~ 8.5 >> 8 ? 0 << 7 > ! "dsf" | ~ ++ 9 <= 5 : 0 )'
    lexer = Lexer(expr)
    parser = ExprParser(lexer)
    tree = parser.expr()
    print(expr)
    print(tree)
