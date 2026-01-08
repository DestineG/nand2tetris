# chapter_7/parser.py

import os
from .templates import templateDict

# 提取伪指令和指令
def extract_instructions(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    instructions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除注释部分
            content = line.split('//')[0]
            # 去除首尾的空白字符（空格、制表符、换行符等）
            clean_line = content.strip()
            # 过滤空行
            if not clean_line:
                continue
            instructions.append(clean_line)
    return instructions

# vm 文件解析
def parse_vm_file(file_path, output_path=None):
    instructions = extract_instructions(file_path)
    current_function_name = ""
    res = []
    
    # --- 添加引导代码 (Bootstrap) ---
    # res.append("// --- Bootstrap Code ---\n")
    # res.append("@256\n"
    #            "D=A\n"
    #            "@SP\n"
    #            "M=D\n")
    
    for inst in instructions:
        splited = inst.split()
        
        # 检查是否为空指令
        if not splited:
            continue

        if splited[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "return"]:
            command = splited[0]
            args = []
        
        elif splited[0] in ["push", "pop"]:
            if len(splited) < 3:
                raise ValueError(f"Invalid {splited[0]} command: expected format '{splited[0]} segment index', got '{inst}'")
            command = f"{splited[0]}_{splited[1]}"
            # 将index转换为整数（pointer和temp需要整数，其他段也需要整数进行地址计算）
            try:
                index = int(splited[2])
            except ValueError:
                raise ValueError(f"Invalid index '{splited[2]}' in {splited[0]} command: must be a number")
            args = [index]
            if splited[1] == "static":
                args.append(os.path.basename(file_path).split('.')[0])
        
        elif splited[0] in ["label", "goto", "if-goto"]:
            if len(splited) < 2:
                raise ValueError(f"Invalid {splited[0]} command: expected format '{splited[0]} label', got '{inst}'")
            assert current_function_name != "", f"{splited[0]} command found before any function declaration"
            command = splited[0]
            args = [current_function_name, splited[1]]
        
        elif splited[0] in ["function", "call"]:
            if len(splited) < 3:
                raise ValueError(f"Invalid {splited[0]} command: expected format '{splited[0]} name n', got '{inst}'")
            command = splited[0]
            # num_locals 和 num_args 需要转换为整数
            try:
                num = int(splited[2])
            except ValueError:
                raise ValueError(f"Invalid number '{splited[2]}' in {splited[0]} command: must be a number")
            args = [splited[1], num]
            if command == "function":
                current_function_name = args[0]
        
        else:
            raise ValueError(f"Unknown command: {splited[0]}")
        
        template_func = templateDict.get(command)
        assert template_func is not None, f"No template found for command: {command} % {splited}"
        res.append(template_func(*args))
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in res:
                f.write(line)
    
    return res
    
if __name__ == "__main__":
    vm_path = r"chapter_7\MemoryAccess\BasicTest\BasicTest.vm"
    output_path = r"chapter_7\MemoryAccess\BasicTest\BasicTest.asm"
    parse_vm_file(vm_path, output_path)