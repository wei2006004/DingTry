TYPE_ID = 'ID'
TYPE_CONST_STRING = 'Const String'
TYPE_CONST_INT = 'Const Int'
TYPE_CONST_FLOAT = 'Const Float'

TYPE_SYMBOL = 'Symbol'
TYPE_KEYWORD = 'Keyword'

CATEGORY_NONE = 0x0

CATEGORY_SY_UNIOP = 0x01
CATEGORY_SY_BINOP = 0x02
CATEGORY_SY_EOF = 0x04

CATEGORY_KW_STMT = 0x10
CATEGORY_KW_BT = 0x20


class Token:
    def __init__(self, type, value, category=CATEGORY_NONE):
        self.type = type
        self.value = value
        self.category = category

    def __repr__(self):
        return "[{type}:{value}:{category}]".format(
            type=self.type,
            value=repr(self.value),
            category=repr(self.category)
        )

    def add_category(self, category):
        self.category |= category

    def match_category(self, category):
        return self.category & category > 0


'''单字符符号定义'''
SY_LPAREN = '('
SY_RPAREN = ')'
SY_LBRACKET = '['
SY_RBRACKET = ']'
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
SY_AND = '&'
SY_OR = '|'
SY_XOR = '^'
SY_COLON = ':'
SY_QUEST = '?'
SY_NOT = '~'
SY_LOG_NOT = '!'

'''单字符符号列表'''
SY_SINGLE_LIST = [SY_LPAREN, SY_RPAREN, SY_LBRACKET, SY_RBRACKET, SY_LBRACE, SY_RBRACE, SY_SEMI,
                  SY_COMMA, SY_ASSIGN, SY_MINUS, SY_PLUS, SY_LESS,
                  SY_GREATER, SY_MUL, SY_DIV, SY_MOD, SY_AND, SY_OR,
                  SY_XOR, SY_COLON, SY_QUEST, SY_NOT, SY_LOG_NOT]

'''双字符符号定义'''
SY_EQUAL = '=='
SY_NOT_EQUAL = '!='
SY_LESS_EQUAL = '<='
SY_GREATER_EQUAL = '>='
SY_ADD_ASSIGN = '+='
SY_MINUS_ASSIGN = '-='
SY_MUL_ASSIGN = '*='
SY_DIV_ASSIGN = '/='
SY_MOD_ASSIGN = '%='
SY_AND_ASSIGN = '&='
SY_OR_ASSIGN = '|='
SY_XOR_ASSIGN = '^='
SY_LSHIFT = '<<'
SY_RSHIFT = '>>'
SY_LOG_AND = '&&'
SY_LOG_OR = '||'
SY_INC = '++'
SY_DEC = '--'

'''双字符符号首字符'''
SY_DOUBLE_HEAD_LIST = ['=', '!', '<', '>', '+', '-', '&', '|']

'''双字符符号列表'''
SY_DOUBLE_LIST = [SY_EQUAL, SY_NOT_EQUAL, SY_LESS_EQUAL, SY_GREATER_EQUAL,
                  SY_ADD_ASSIGN, SY_MINUS_ASSIGN, SY_LSHIFT, SY_RSHIFT, SY_LOG_AND,
                  SY_LOG_OR, SY_MUL_ASSIGN, SY_DIV_ASSIGN, SY_MOD_ASSIGN, SY_AND_ASSIGN,
                  SY_OR_ASSIGN, SY_XOR_ASSIGN, SY_INC, SY_DEC]

SY_EOF = 'EOF'

'''双目运算符，从左到右，优先级从高到低'''
BINOP_LIST = [SY_MUL, SY_DIV, SY_MOD, SY_PLUS, SY_MINUS, SY_LSHIFT, SY_RSHIFT,
              SY_GREATER, SY_GREATER_EQUAL, SY_LESS, SY_LESS_EQUAL, SY_EQUAL, SY_NOT_EQUAL,
              SY_AND, SY_XOR, SY_OR, SY_LOG_AND, SY_LOG_OR]

'''单目运算符，从右到左'''
UNIOP_LIST = [SY_PLUS, SY_MINUS, SY_INC, SY_DEC, SY_NOT, SY_LOG_NOT]


class SyToken(Token):
    def __init__(self, value, category=CATEGORY_NONE):
        Token.__init__(self, TYPE_SYMBOL, value, category)
        self.init_category()

    def init_category(self):
        if self.value in BINOP_LIST:
            self.add_category(CATEGORY_SY_BINOP)
        if self.value in UNIOP_LIST:
            self.add_category(CATEGORY_SY_UNIOP)
        if self.value is SY_EOF:
            self.add_category(CATEGORY_SY_EOF)


SY_MAP = {SY_EOF: SyToken(SY_EOF)}

for sy in SY_SINGLE_LIST:
    SY_MAP[sy] = SyToken(sy)

for sy in SY_DOUBLE_LIST:
    SY_MAP[sy] = SyToken(sy)

'''关键字定义'''
KW_DEF = 'def'
KW_VAR = 'var'
KW_DO = 'do'
KW_WHILE = 'while'
KW_IF = 'if'
KW_ELSE = 'else'
KW_FOR = 'for'
KW_SWITCH = 'switch'
KW_CASE = 'case'
KW_RETURN = 'return'

KW_STRING = 'string'
KW_INT = 'int'
KW_FLOAT = 'float'
KW_DOUBLE = 'double'
KW_BOOL = 'bool'
KW_CHAR = 'char'

'''关键字列表'''
KW_LIST = [KW_DEF, KW_VAR, KW_DO, KW_WHILE, KW_IF,
           KW_ELSE, KW_FOR, KW_SWITCH, KW_CASE, KW_RETURN,
           KW_STRING, KW_INT, KW_FLOAT, KW_DOUBLE, KW_BOOL, KW_CHAR]
KW_BT_LIST = [KW_STRING, KW_INT, KW_FLOAT, KW_DOUBLE, KW_BOOL, KW_CHAR]
KW_STMT_LIST = [KW_DO, KW_WHILE, KW_IF, KW_FOR, KW_SWITCH]


class KwToken(Token):
    def __init__(self, value, category=CATEGORY_NONE):
        Token.__init__(self, TYPE_KEYWORD, value, category)
        self.init_category()

    def init_category(self):
        if self.value in KW_BT_LIST:
            self.add_category(CATEGORY_KW_BT)
        if self.value in KW_STMT_LIST:
            self.add_category(CATEGORY_KW_STMT)


KW_MAP = {}
for kw in KW_LIST:
    KW_MAP[kw] = KwToken(kw)

if __name__ == '__main__':
    print(SY_MAP)
    print(KW_MAP)
