# test/test.py

import os
from ..utils.fileio import read_jack_file, write_vm_file


if __name__ == "__main__":
    # 简单测试
    jack_path = 'inputs/Square.jack'
    build_dir = 'build/'
    
    jack_lines = read_jack_file(jack_path)
    print("读取的 Jack 文件内容:")
    for line in jack_lines:
        print(line.strip())

    vm_code = [
        "function Main.main 0",
        "push constant 0",
        "call Sys.init 0",
        "return"
    ]
    write_vm_file(os.path.join(build_dir, 'Example.vm'), vm_code)
    print("VM 代码已写入 Example.vm")