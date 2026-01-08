# chapter_7/templates.py

templateDict = {
}

class Arithmetic:
    counter = -1
    def __init__(self):
        templateDict["add"] = Arithmetic.add
        templateDict["sub"] = Arithmetic.sub
        templateDict["neg"] = Arithmetic.neg
        templateDict["and"] = Arithmetic.and_
        templateDict["or"] = Arithmetic.or_
        templateDict["not"] = Arithmetic.not_
        templateDict["eq"] = Arithmetic.eq
        templateDict["gt"] = Arithmetic.gt
        templateDict["lt"] = Arithmetic.lt

    # 将栈顶的两个元素相加(addr(SP-2) + addr(SP-1))，结果放回栈顶，栈指针减1
    @staticmethod
    def add():
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"M=D+M\n"
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
    def eq():
        Arithmetic.counter += 1
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@EQ_TRUE_{Arithmetic.counter}\n"
            f"D;JEQ\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@EQ_END_{Arithmetic.counter}\n"
            f"0;JMP\n"
            f"(EQ_TRUE_{Arithmetic.counter})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(EQ_END_{Arithmetic.counter})\n"
        )
    
    # 将栈顶的两个元素比较是否大于(addr(SP-2) > addr(SP-1))，结果放回栈顶，栈指针减1，大于为 -1，不大于为 0
    @staticmethod
    def gt():
        Arithmetic.counter += 1
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@GT_TRUE_{Arithmetic.counter}\n"
            f"D;JGT\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@GT_END_{Arithmetic.counter}\n"
            f"0;JMP\n"
            f"(GT_TRUE_{Arithmetic.counter})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(GT_END_{Arithmetic.counter})\n"
        )
    
    # 将栈顶的两个元素比较是否小于(addr(SP-2) < addr(SP-1))，结果放回栈顶，栈指针减1，小于为 -1，不小于为 0
    @staticmethod
    def lt():
        Arithmetic.counter += 1
        return (
            f"@SP\n"
            f"A=M-1\n"
            f"D=M\n"
            f"A=A-1\n"
            f"D=M-D\n"
            f"@SP\n"
            f"M=M-1\n"
            f"@LT_TRUE_{Arithmetic.counter}\n"
            f"D;JLT\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=0\n"
            f"@LT_END_{Arithmetic.counter}\n"
            f"0;JMP\n"
            f"(LT_TRUE_{Arithmetic.counter})\n"
            f"@SP\n"
            f"A=M-1\n"
            f"M=-1\n"
            f"(LT_END_{Arithmetic.counter})\n"
        )

class MemoryAccess:
    def __init__(self):
        templateDict["push_constant"] = MemoryAccess.push_constant
        templateDict["push_local"] = MemoryAccess.push_local
        templateDict["push_argument"] = MemoryAccess.push_argument
        templateDict["push_this"] = MemoryAccess.push_this
        templateDict["push_that"] = MemoryAccess.push_that
        templateDict["pop_local"] = MemoryAccess.pop_local
        templateDict["pop_argument"] = MemoryAccess.pop_argument
        templateDict["pop_this"] = MemoryAccess.pop_this
        templateDict["pop_that"] = MemoryAccess.pop_that
        templateDict["push_temp"] = MemoryAccess.push_temp
        templateDict["pop_temp"] = MemoryAccess.pop_temp
        templateDict["push_pointer"] = MemoryAccess.push_pointer
        templateDict["pop_pointer"] = MemoryAccess.pop_pointer
        templateDict["push_static"] = MemoryAccess.push_static
        templateDict["pop_static"] = MemoryAccess.pop_static

    @staticmethod
    def push_constant(value):
        return (
            f"@{value}\n"
            f"D=A\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )
    
    @staticmethod
    def push_local(index):
        return (
            f"@LCL\n"
            f"D=M\n"
            f"@{index}\n"
            f"A=D+A\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )
    
    @staticmethod
    def push_argument(index):
        return (
            f"@ARG\n"
            f"D=M\n"
            f"@{index}\n"
            f"A=D+A\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )

    @staticmethod
    def push_this(index):
        return (
            f"@THIS\n"
            f"D=M\n"
            f"@{index}\n"
            f"A=D+A\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )

    @staticmethod
    def push_that(index):
        return (
            f"@THAT\n"
            f"D=M\n"
            f"@{index}\n"
            f"A=D+A\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )

    @staticmethod
    def pop_local(index):
        return (
            # 计算 local index 的地址 -> D -> R13
            f"@LCL\n"
            f"D=M\n"
            f"@{index}\n"
            f"D=D+A\n"
            f"@R13\n"
            f"M=D\n"

            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            #  R13 -> A
            f"@R13\n"
            f"A=M\n"

            # D -> M
            f"M=D\n"
        )
    
    @staticmethod
    def pop_argument(index):
        return (
            # 计算 ARG index 的地址 -> D -> R13
            f"@ARG\n"
            f"D=M\n"
            f"@{index}\n"
            f"D=D+A\n"
            f"@R13\n"
            f"M=D\n"

            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            #  R13 -> A
            f"@R13\n"
            f"A=M\n"

            # D -> M
            f"M=D\n"
        )
    
    @staticmethod
    def pop_this(index):
        return (
            # 计算 THIS index 的地址 -> D -> R13
            f"@THIS\n"
            f"D=M\n"
            f"@{index}\n"
            f"D=D+A\n"
            f"@R13\n"
            f"M=D\n"

            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            #  R13 -> A
            f"@R13\n"
            f"A=M\n"

            # D -> M
            f"M=D\n"
        )
    
    @staticmethod
    def pop_that(index):
        return (
            # 计算 THAT index 的地址 -> D -> R13
            f"@THAT\n"
            f"D=M\n"
            f"@{index}\n"
            f"D=D+A\n"
            f"@R13\n"
            f"M=D\n"

            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            #  R13 -> A
            f"@R13\n"
            f"A=M\n"

            # D -> M
            f"M=D\n"
        )
    
    @staticmethod
    def push_temp(index):
        return (
            f"@{5 + index}\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )

    @staticmethod
    def pop_temp(index):
        return (
            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            f"@{5 + index}\n"
            f"M=D\n"
        )
    
    @staticmethod
    def push_pointer(index):
        return (
            f"@{'THIS' if index == 0 else 'THAT'}\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )
    
    @staticmethod
    def pop_pointer(index):
        return (
            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            f"@{'THIS' if index == 0 else 'THAT'}\n"
            f"M=D\n"
        )
    
    @staticmethod
    def push_static(index, filename):
        return (
            f"@{filename}.{index}\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
        )
    
    @staticmethod
    def pop_static(index, filename):
        return (
            # SP-- & 从栈顶取数据 -> D
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"

            f"@{filename}.{index}\n"
            f"M=D\n"
        )

class ProgramFlow:
    def __init__(self):
        templateDict["label"] = ProgramFlow.label
        templateDict["goto"] = ProgramFlow.goto
        templateDict["if-goto"] = ProgramFlow.if_goto

    @staticmethod
    def label(current_function, label_name):
        return (
            f"({current_function}${label_name})\n"
        )

    @staticmethod
    def goto(current_function, label_name):
        return (
            f"@{current_function}${label_name}\n"
            f"0;JMP\n"
        )
    
    @staticmethod
    def if_goto(current_function, label_name):
        return (
            # SP-- & 从栈顶取数据 -> D
            # 如果 D != 0 则跳转到 label_name
            # 也就是栈顶元素不为零时跳转
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@{current_function}${label_name}\n"
            f"D;JNE\n"
        )

class FunctionCalling:
    call_idx = 0
    def __init__(self):
        templateDict["function"] = FunctionCalling.function
        templateDict["call"] = FunctionCalling.call
        templateDict["return"] = FunctionCalling.ret

    @staticmethod
    def function(function_name, num_locals):
        return (
            f"({function_name})\n"
            + "".join(
                MemoryAccess.push_constant(0)
                for _ in range(int(num_locals))
            )
        )
    
    @staticmethod
    def call(function_name, num_args):
        ret_label = f"{function_name}$ret.{FunctionCalling.call_idx}"
        FunctionCalling.call_idx += 1
        return (
            # 推入返回地址
            f"@{ret_label}\n"
            f"D=A\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
            # 推入 LCL
            f"@LCL\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
            # 推入 ARG
            f"@ARG\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
            # 推入 THIS
            f"@THIS\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
            # 推入 THAT
            f"@THAT\n"
            f"D=M\n"
            f"@SP\n"
            f"A=M\n"
            f"M=D\n"
            f"@SP\n"
            f"M=M+1\n"
            # ARG = SP - num_args - 5
            f"@SP\n"
            f"D=M\n"
            f"@{int(num_args) + 5}\n"
            f"D=D-A\n"
            f"@ARG\n"
            f"M=D\n"
            # LCL = SP
            f"@SP\n"
            f"D=M\n"
            f"@LCL\n"
            f"M=D\n"
            # 跳转到函数
            f"@{function_name}\n"
            f"0;JMP\n"
            # 返回地址标签
            f"({ret_label})\n"
        )
    
    @staticmethod
    def ret():
        return (
            # 找到恢复现场的地址 R13 = LCL
            f"@LCL\n"
            f"D=M\n"
            f"@R13\n"
            f"M=D\n"
            # 获取返回地址 R14 = RET = *(FRAME - 5)
            f"@5\n"
            f"A=D-A\n"
            f"D=M\n"
            f"@R14\n"
            f"M=D\n"
            # 获取返回值 *(func_ARG + 0) = pop()；函数返回值放到调用者的栈顶
            f"@SP\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@ARG\n"
            f"A=M\n"
            f"M=D\n"
            # 恢复栈顶指针 SP = func_ARG + 1
            f"@ARG\n"
            f"D=M+1\n"
            f"@SP\n"
            f"M=D\n"
            # 恢复 THAT = *(FRAME - 1)
            f"@R13\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@THAT\n"
            f"M=D\n"
            # 恢复 THIS = *(FRAME - 2)
            f"@R13\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@THIS\n"
            f"M=D\n"
            # 恢复 ARG = *(FRAME - 3)
            f"@R13\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@ARG\n"
            f"M=D\n"
            # 恢复 LCL = *(FRAME - 4)
            f"@R13\n"
            f"M=M-1\n"
            f"A=M\n"
            f"D=M\n"
            f"@LCL\n"
            f"M=D\n"
            # 跳转到返回地址 RET
            f"@R14\n"
            f"A=M\n"
            f"0;JMP\n"
        )

def init_templates():
    Arithmetic()
    MemoryAccess()
    ProgramFlow()
    FunctionCalling()
init_templates()