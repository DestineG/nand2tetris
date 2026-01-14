import os
import sys
from .parser.parser import Parser

def compile_directory(path):
    # 确保路径存在
    if not os.path.isdir(path):
        print("Path is not a directory.")
        return

    # 找到所有的 .jack 文件
    jack_files = [f for f in os.listdir(path) if f.endswith('.jack')]

    for jack_file in jack_files:
        input_path = os.path.join(path, jack_file)
        # 生成对应的 .vm 文件路径
        out_dir = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\build"
        output_path = os.path.join(out_dir, jack_file.replace('.jack', '.vm'))
        
        print(f"Compiling {jack_file}...")
        
        # 初始化 Parser (注意：你需要修改 Parser 让它接受 output_path 作为 codegen 的参数)
        parser = Parser(input_path, output_path)
        parser.compile_class()

    print("All files compiled successfully.")

if __name__ == "__main__":
    # 使用方式: python -m chapter_11.src.main D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs
    if len(sys.argv) > 1:
        compile_directory(sys.argv[1])
    else:
        print("Please provide a directory path.")