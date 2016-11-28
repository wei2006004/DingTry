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


class ExprParser(Parser):
    def factor(self):
        value = self.current_token.value
        self.eat(type=TYPE_CONST_INT)
        return int(value)

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


if __name__ == '__main__':
    print(BINOP_LIST)
    print(UNIOP_LIST)
    from _lexer import Lexer

    expr = '2 + 3 ? 9 / 2 - 5 * 6 | - 1 : 6 && ~ 8 >> 8 ? 0 << 7 > ! ~ ++ 9 <= 5 : 0 & 6'
    lexer = Lexer(expr)
    parser = ExprParser(lexer)
    tree = parser.expr()
    print(expr)
    print(tree)
