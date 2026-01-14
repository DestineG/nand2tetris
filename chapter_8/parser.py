# chapter_8/VMTranslator.py

import os
from chapter_6.parser import hack_assembler
from chapter_7.parser import parse_vm_file
from chapter_7.templates import templateDict

def generate_bootstrap_code(enterPoint):
    # 物理段指针初始化
    init_pointers_data = [
        ("SP", 256),
        ("LCL", 300),
        ("ARG", 400),
        ("THIS", 3000),
        ("THAT", 4000)
    ]
    
    asm_lines = ["// --- Bootstrap: Segment Initialization ---\n"]
    for segment, value in init_pointers_data:
        asm_lines.append(
            (
                f"@{value}\n"
                f"D=A\n"
                f"@{segment}\n"
                f"M=D\n"
            )
        ) 

    # enterPoint call
    if enterPoint:
        asm_lines.append(f"// --- Bootstrap: Calling {enterPoint} ---\n")
        build_call = templateDict.get("call")
        enterPointCode = build_call(enterPoint, 0)
        asm_lines.append("".join(enterPointCode))

    return "".join(asm_lines)

def vm_translator(input_path, output_path):
    enterPoint = "Sys.init"
    enterPointFound = False
    vm2asm_output = ""
    if input_path.endswith('.vm'):
        # 单个 VM 文件处理
        print(f"Translating single VM file: {input_path}")
        asm = parse_vm_file(input_path, None)
        asmString = ''.join(asm)
        vm2asm_output += asmString
        if enterPoint in asmString:
            enterPointFound = True

    elif os.path.isdir(input_path):
        # 多 VM 文件处理
        print(f"Translating all VM files in directory: {input_path}")
        for filename in os.listdir(input_path):
            if filename.endswith('.vm'):
                vm_file_path = os.path.join(input_path, filename)
                asm = parse_vm_file(vm_file_path, None)
                asmString = ''.join(asm)
                vm2asm_output += asmString
                if enterPoint in asmString:
                    enterPointFound = True

    else:
        raise ValueError(f"Input path {input_path} is neither a .vm file nor a directory.")
    
    if enterPointFound:
        bootstrap_code = generate_bootstrap_code(enterPoint)
    else:
        bootstrap_code = generate_bootstrap_code(None)

    final_asm = bootstrap_code + vm2asm_output
    if output_path and output_path.endswith('.asm'):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_asm)

    if output_path and output_path.endswith('.hack'):
        temp_asm_path = output_path.replace('.hack', '.asm')
        with open(temp_asm_path, 'w', encoding='utf-8') as f:
            f.write(final_asm)
        final_bin = hack_assembler(temp_asm_path, output_path)
        os.remove(temp_asm_path)
        return final_bin

    return final_asm


if __name__ == "__main__":
    input_path = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs\Main.vm"
    output_path = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs\Main.hack"
    vm_translator(input_path, output_path)