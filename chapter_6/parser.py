# chapter_6/parser.py

import os
import argparse

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

# 伪指令提取 使用()进行匹配
def extract_pseudo_instructions(instructions):
    pure_instructions = []
    pseudo_instructions = []
    for ind, instruction in enumerate(instructions):
        if instruction.startswith('(') and instruction.endswith(')'):
            pseudo_instructions.append((instruction[1:-1].strip(), ind - len(pseudo_instructions)))
        else:
            pure_instructions.append(instruction)
    return pseudo_instructions, pure_instructions

# 用 pseudo_instructions, pure_instructions 构建符号表
def build_symbol_table(pseudo_instructions, pure_instructions):
    symbol_table = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        'SCREEN': 16384,
        'KBD': 24576
    }
    # 添加预定义寄存器到符号表
    for i in range(16):
        symbol_table[f'R{i}'] = i
    # 添加伪指令到符号表 value 为对应的跳转地址(指令存储器)
    for symbol, address in pseudo_instructions:
        symbol_table[symbol] = address
    # 添加变量到符号表 value为变量所在内存地址(数据存储器)
    next_variable_address = 16
    for instruction in pure_instructions:
        if instruction.startswith('@'):
            symbol = instruction[1:]
            if not symbol.isdigit() and symbol not in symbol_table:
                symbol_table[symbol] = next_variable_address
                next_variable_address += 1
    return symbol_table

# 符号替换 将伪指令符号变量符号预变量符号
def replace_symbols(pure_instructions, symbol_table):
    replaced_instructions = []
    for instruction in pure_instructions:
        # A 指令处理
        if instruction.startswith('@'):
            symbol = instruction[1:]
            if symbol.isdigit():
                replaced_instructions.append(instruction)
            else:
                address = symbol_table.get(symbol)
                replaced_instructions.append(f"@{address}")
        # C 指令处理
        else:
            replaced_instructions.append(instruction)
    return replaced_instructions

# 解析 A 指令
def parse_a_instruction(instruction):
    if not instruction.startswith('@'):
        raise ValueError("Not an A-instruction")
    symbol = instruction[1:]
    if not symbol.isdigit():
        raise ValueError("A-instruction does not contain a numeric value")
    address = int(symbol) & 0x7FFF
    return f"0{address:015b}"

def translate_c_instruction(dest, comp, jump):
    comp_table = {
        '0':   '0101010',
        '1':   '0111111',
        '-1':  '0111010',
        'D':   '0001100',
        'A':   '0110000',
        '!D':  '0001101',
        '!A':  '0110001',
        '-D':  '0001111',
        '-A':  '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M':   '1110000',
        '!M':  '1110001',
        '-M':  '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101'
    }
    dest_table = {
        '':    '000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111'
    }
    jump_table = {
        '':    '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    comp_bits = comp_table.get(comp)
    dest_bits = dest_table.get(dest)
    jump_bits = jump_table.get(jump)
    if comp_bits is None or dest_bits is None or jump_bits is None:
        raise ValueError("Invalid C-instruction components")
    return f"111{comp_bits}{dest_bits}{jump_bits}"

# 解析 C 指令
def parse_c_instruction(instruction):
    dest = ""
    comp = ""
    jump = ""

    #  dest=comp;jump
    # 尝试拆分分号
    if ";" in instruction:
        temp, jump = instruction.split(";")
    else:
        temp = instruction

    # 尝试拆分等号 (处理 dest 和 comp)
    if "=" in temp:
        dest, comp = temp.split("=")
    else:
        comp = temp
    return translate_c_instruction(
        dest.replace(" ", ""),
        comp.replace(" ", ""),
        jump.replace(" ", "")
    )

def hack_assembler(input_file, output_file=None):
    if os.path.exists(input_file) is False:
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    instructions = extract_instructions(input_file)
    pseudo_instructions, pure_instructions = extract_pseudo_instructions(instructions)
    symbol_table = build_symbol_table(pseudo_instructions, pure_instructions)
    replaced_instructions = replace_symbols(pure_instructions, symbol_table)
    
    machine_code = []
    for instruction in replaced_instructions:
        if instruction.startswith('@'):
            binary = parse_a_instruction(instruction)
        else:
            binary = parse_c_instruction(instruction)
        machine_code.append(binary)
    
    if output_file:
        with open(output_file, 'w') as f:
            for code in machine_code:
                f.write(code + '\n')
    return machine_code

# python chapter_6/parser.py chapter_6/Mult.asm -o chapter_6/Mult.hack
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hack Assembler")
    parser.add_argument("input_file", help="Path to the input .asm file")
    parser.add_argument("-o", "--output_file", help="Path to the output .hack file")
    args = parser.parse_args()

    # 自动处理输出文件名逻辑
    target_output = args.output_file
    if not target_output:
        target_output = args.input_file.replace(".asm", ".hack")
        if target_output == args.input_file:
            target_output += ".hack"

    machine_code = hack_assembler(args.input_file, output_file=target_output)
    
    print(f"Parsing completed. Target: {target_output}")