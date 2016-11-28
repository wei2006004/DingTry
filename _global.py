TYPE_ID = 'ID'
TYPE_CONST_STRING = 'Const String'
TYPE_CONST_INT = 'Const Int'
TYPE_CONST_FLOAT = 'Const Float'

TYPE_SYMBOL = 'Symbol'
TYPE_KEYWORD = 'Keyword'
TYPE_BUILDIN_TYPE = 'Buildin Type'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "[{type}:{value}]".format(
            type=self.type,
            value=repr(self.value)
        )


class SyToken(Token):
    def __init__(self, value):
        Token.__init__(self, TYPE_SYMBOL, value)


class KwToken(Token):
    def __init__(self, value):
        Token.__init__(self, TYPE_KEYWORD, value)


class BtToken(Token):
    def __init__(self, value):
        Token.__init__(self, TYPE_BUILDIN_TYPE, value)


SY_LPAREN = '('
SY_RPAREN = ')'
SY_LBRACE = '{'
SY_RBRACE = '}'
SY_SEMI = ';'
SY_COMMA = ','
SY_ASSIGN = '='
SY_PLUS = '+'
SY_MINUS = '-'
SY_MUL = '*'
SY_DIV = '/'
SY_MOD = '%'
SY_LESS = '<'
SY_GREATER = '>'

SY_SINGLE_LIST = [SY_LPAREN, SY_RPAREN, SY_LBRACE, SY_RBRACE, SY_SEMI, SY_COMMA, SY_ASSIGN, SY_MINUS, SY_PLUS, SY_LESS,
                  SY_GREATER, SY_MUL, SY_DIV, SY_MOD]

SY_EQUAL = '=='
SY_NOT_EQUAL = '!='
SY_LESS_EQUAL = '<='
SY_GREATER_EQUAL = '>='
SY_ACCUM = '+='
SY_REDUCT = '-='

SY_DOUBLE_HEAD_LIST = ['=', '!', '<', '>', '+', '-']    # 可能为双字符符号的头字符
SY_DOUBLE_LIST = [SY_EQUAL, SY_NOT_EQUAL, SY_LESS_EQUAL, SY_GREATER_EQUAL, SY_ACCUM, SY_REDUCT]

SY_EOF = 'EOF'
SY_MAP = {SY_EOF: SyToken(SY_EOF)}

for sy in SY_SINGLE_LIST:
    SY_MAP[sy] = SyToken(sy)

for sy in SY_DOUBLE_LIST:
    SY_MAP[sy] = SyToken(sy)

KW_DEF = 'def'

KW_LIST = [KW_DEF]
KW_MAP = {}
for kw in KW_LIST:
    KW_MAP[kw] = KwToken(kw)

BT_STRING = 'string'
BT_INT = 'int'
BT_FLOAT = 'float'
BT_DOUBLE = 'double'
BT_BOOL = 'bool'
BT_CHAR = 'char'

BT_LIST = [BT_STRING, BT_INT, BT_FLOAT, BT_DOUBLE, BT_BOOL, BT_CHAR]
BT_MAP = {}
for bt in BT_LIST:
    BT_MAP[bt] = BtToken(bt)

if __name__ == '__main__':
    print(SY_MAP)
    print(KW_MAP)
    print(BT_MAP)
