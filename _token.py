TYPE_ID = 'ID'
TYPE_CONST_STRING = 'CONST_STRING'

TYPE_SY_LPAREN = 'LPAREN'
TYPE_SY_RPAREN = 'RPAREN'
TYPE_SY_LBRACE = 'LBRACE'
TYPE_SY_RBRACE = 'RBRACE'
TYPE_SY_SEMI = 'SEMI'
TYPE_SY_EOF = 'EOF'

TYPE_KW_DEF = 'def'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "Token: {type} {value}".format(
            type=self.type,
            value=repr(self.value)
        )