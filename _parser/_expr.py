from ._base import *

BINOP_LIST = [{SY_MUL, SY_DIV, SY_MOD},
              {SY_PLUS, SY_MINUS},
              {},
              {},
              {},
              {},
              {}]


class BinOp(AST):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right


class ExprParser(Parser):
    def expr(self):
        pass
