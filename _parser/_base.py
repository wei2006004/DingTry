from _global import *

BLOCK_TYPE_STMT = 0x01
BLOCK_TYPE_FUNCTION = 0x02
BLOCK_TYPE_CLASS = 0x03
BLOCK_TYPE_METHOD = 0x04
BLOCK_TYPE_FILE = 0x05

VAR_TYPE_LOCAL = 0x01
VAR_TYPE_FUNCTION = 0x02
VAR_TYPE_ARGUMENT = 0x03
VAR_TYPE_FIELD = 0x04
VAR_TYPE_METHOD = 0x05

ASSESS_TYPE_PUBLIC = 0x01
ASSESS_TYPE_PROTECT = 0x02
ASSESS_TYPE_PRIVATE = 0x03
ASSESS_TYPE_PACKAGE = 0x04


class AST:
    def __repr__(self):
        return '\n' + str(self.__class__) + '\n' + repr(self.__dict__)


class Class:
    def __init__(self, package, name, assess_type=ASSESS_TYPE_PACKAGE):
        self.package = package
        self.name = name
        self.assess_type = assess_type


class Variable(AST):
    def __init__(self, name, clazz, block, type):
        self.name = name
        self.clazz = clazz
        self.block = block
        self.type = type

    def is_method(self):
        return self.type is VAR_TYPE_METHOD

    def is_function(self):
        return self.type is VAR_TYPE_FUNCTION

    def is_local_var(self):
        return self.type is VAR_TYPE_LOCAL

    def is_argument(self):
        return self.type is VAR_TYPE_ARGUMENT

    def is_field(self):
        return self.type is VAR_TYPE_FIELD

    def __repr__(self):
        return '(Var ' + self.name + ':' + repr(self.clazz) + ':' + repr(self.type) + ')'


class Block(AST):
    def __init__(self, parent, package, type=BLOCK_TYPE_STMT):
        self.parent = parent
        self.stmts = []
        self.vars = {}
        self.classes = {}
        self.package = package
        self.type = type

    def add_stmt(self, stmt):
        self.stmts.append(stmt)

    def add_stmts(self, stmts):
        self.stmts += stmts

    def is_function_block(self):
        return self.type is BLOCK_TYPE_FUNCTION

    def is_class_block(self):
        return self.type is BLOCK_TYPE_CLASS

    def is_stmt_block(self):
        return self.type is BLOCK_TYPE_STMT

    def is_method_block(self):
        return self.type is BLOCK_TYPE_METHOD

    def add_var(self, name, clazz, type):
        self.vars[name] = Variable(name, clazz, self, type)

    def add_local_var(self, name, clazz):
        self.vars[name] = Variable(name, clazz, self, VAR_TYPE_LOCAL)

    def add_function(self, name, clazz=KW_MAP[KW_VOID]):
        self.vars[name] = Variable(name, clazz, self, VAR_TYPE_FUNCTION)

    def add_class(self, name, package, type=ASSESS_TYPE_PACKAGE):
        self.classes[package + '.' + name] = Class(package, name, type)

    def get_class_recur(self, name, package):
        entire_name = package + '.' + name
        return self.get_class_recur_by_entire_name(entire_name)

    def get_class_recur_by_entire_name(self, entire_name):
        block = self
        while block is not None:
            if block.contains_class(entire_name):
                return block.get_class(entire_name)
            block = block.parent
        return None

    def contains_class(self, entire_name):
        return entire_name in self.classes.keys()

    def get_class(self, entire_name):
        return self.classes[entire_name]

    def contains_var_recur(self, name):
        block = self
        while block is not None:
            if block.contains_var(name):
                return True
            block = block.parent
        return False

    def get_var_recur(self, name):
        block = self
        while block is not None:
            if block.contains_var(name):
                return block.get_var(name)
            block = block.parent
        return None

    def contains_var(self, name):
        return name in self.vars.keys()

    def get_var(self, name):
        return self.vars[name]

    def __repr__(self):
        ret = '{\n'
        for stmt in self.stmts:
            ret += repr(stmt)
            ret += '\n'
        ret += '} ['
        for var in self.vars.values():
            ret += repr(var)
            ret += '\t'
        ret += ']\n'
        return ret


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, value=None, type=None, category=CATEGORY_NONE):
        if value and self.current_token.value is not value:
            self.error()
        if type and self.current_token.type is not type:
            self.error()
        if category is not CATEGORY_NONE and not self.current_token.match_category(category):
            self.error()
        self.next_token()

    def eat_id(self, id=None, category=CATEGORY_NONE):
        self.eat(value=id, type=TYPE_ID, category=category)

    def eat_sy(self, symbol=None, category=CATEGORY_NONE):
        self.eat(value=symbol, type=TYPE_SYMBOL, category=category)

    def eat_kw(self, key=None, category=CATEGORY_NONE):
        self.eat(value=key, type=TYPE_KEYWORD, category=category)

    def error(self, msg=None):
        text = 'Invalid syntax'
        if msg:
            text += ': ' + msg
        else:
            text += repr(self.current_token)
        raise Exception(text)

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
