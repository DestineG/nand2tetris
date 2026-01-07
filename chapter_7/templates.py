# chapter_7/templates.py

class Arithmetic:
    def __init__(self):
        pass

    # 将栈顶的两个元素相加(addr(SP-2) + addr(SP-1))，结果放回栈顶，栈指针减1
    @staticmethod
    def add():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"M=M+D\n"
            f"@SP\n"
            f"M=M-1\n"
        )
    
    # 将栈顶的两个元素相减(addr(SP-2) - addr(SP-1))，结果放回栈顶，栈指针减1
    @staticmethod
    def sub():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"M=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
        )
    
    # 将栈顶元素取负，结果放回栈顶
    @staticmethod
    def neg():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"M=-M\n"
        )
    
    # 将栈顶的两个元素做与运算，结果放回栈顶，栈指针减1
    @staticmethod
    def and_():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"M=M&D\n"
            f"@SP\n"
            f"M=M-1\n"
        )
    
    # 将栈顶的两个元素做或运算，结果放回栈顶，栈指针减1
    @staticmethod
    def or_():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"M=M|D\n"
            f"@SP\n"
            f"M=M-1\n"
        )
    
    # 将栈顶元素按位取反，结果放回栈顶
    @staticmethod
    def not_():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"M=!M\n"
        )

    # 将栈顶的两个元素比较是否相等(addr(SP-2) = addr(SP-1))，结果放回栈顶，栈指针减1，相等为 -1，不等为 0
    @staticmethod
    def eq(index):
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@EQ_TRUE_{index}\n"
            f"D;JEQ\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@EQ_END_{index}\n"
            f"0;JMP\n"
            f"(EQ_TRUE_{index})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(EQ_END_{index})\n"
        )
    
    # 将栈顶的两个元素比较是否大于(addr(SP-2) > addr(SP-1))，结果放回栈顶，栈指针减1，大于为 -1，不大于为 0
    @staticmethod
    def gt(index):
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@GT_TRUE_{index}\n"
            f"D;JGT\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@GT_END_{index}\n"
            f"0;JMP\n"
            f"(GT_TRUE_{index})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(GT_END_{index})\n"
        )
    
    # 将栈顶的两个元素比较是否小于(addr(SP-2) < addr(SP-1))，结果放回栈顶，栈指针减1，小于为 -1，不小于为 0
    @staticmethod
    def lt(index):
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@LT_TRUE_{index}\n"
            f"D;JLT\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@LT_END_{index}\n"
            f"0;JMP\n"
            f"(LT_TRUE_{index})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(LT_END_{index})\n"
        )


print(Arithmetic.eq(1))