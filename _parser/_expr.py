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


class BinOp(AST):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        return '(' + self.operation + ': ' + repr(self.left) + ', ' + repr(self.right) + ')'


class ExprParser(Parser):
    def factor(self):
        value = self.current_token.value
        self.eat(type=TYPE_CONST_INT)
        return int(value)

    def expr(self):
        return self.create_binop(len(BINOP_LIST))

    def create_binop(self, index):
        if index == 0:
            return self.factor()
        tree = self.create_binop(index - 1)
        while self.current_token.value is not SY_EOF and self.current_token.value in BINOP_LIST[index - 1]:
            operation = self.current_token.value
            self.eat_binop(index - 1)
            right = self.create_binop(index - 1)
            if right is None:
                self.error('right is empty:' + operation)
            tree = BinOp(operation, tree, right)
        return tree

    def eat_binop(self, index):
        if self.current_token.value not in BINOP_LIST[index]:
            self.error('index:' + index + ' value:' + self.current_token.value)
        self.eat_sy()


if __name__ == '__main__':
    print(BINOP_LIST)
    from _lexer import Lexer
    lexer = Lexer('2 + 3 / 2 - 5 * 6 | 6 && 8 >> 8 << 7 > 9 <= 5 & 6')
    parser = ExprParser(lexer)
    tree = parser.expr()
    print(tree)
