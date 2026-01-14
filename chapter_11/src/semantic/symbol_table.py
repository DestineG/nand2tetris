# src/semantic/symbol_table.py

class SymbolTable:
    def __init__(self):
        # 类作用域符号表
        self.class_scope = {}
        # 子程序作用域符号表
        self.subroutine_scope = {}
        # 用于记录每种变量的索引
        self.index_counters = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0
        }

    # 开始处理一个新的子程序，重置子程序级别的符号表
    def start_subroutine(self):
        self.subroutine_scope = {}
        self.index_counters['arg'] = 0
        self.index_counters['var'] = 0

    # 在符号表中定义一个新标识符
    def define(self, name, var_type, kind):
        index = self.index_counters[kind]
        if kind in ('static', 'field'):
            self.class_scope[name] = (var_type, kind, index)
        else:
            self.subroutine_scope[name] = (var_type, kind, index)
        self.index_counters[kind] += 1

    # 返回给定种类的变量数量
    def var_count(self, kind):
        return self.index_counters[kind]

    # 返回标识符的种类
    def kind_of(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][1]
        elif name in self.class_scope:
            return self.class_scope[name][1]
        else:
            return None

    # 返回标识符的类型
    def type_of(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][0]
        elif name in self.class_scope:
            return self.class_scope[name][0]
        else:
            return None

    # 返回标识符的索引
    def index_of(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][2]
        elif name in self.class_scope:
            return self.class_scope[name][2]
        else:
            return None