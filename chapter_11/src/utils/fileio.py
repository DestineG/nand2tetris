# chapter_11/utils/fileio.py

from typing import List

# demo jack file
demo_jack_file = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs\Square.jack"

def read_jack_file(file_path) -> List[str]:
    """
    读取指定路径的 .jack 文件内容

    参数:
        file_path (str): .jack 文件的路径

    返回:
        List[str]: 文件内容按行分割的字符串列表
    """
    if file_path is None:
        file_path = demo_jack_file
    assert file_path.endswith('.jack'), f"文件必须是 .jack 格式，但得到 {file_path}"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
    except Exception as e:
        raise IOError(f"无法读取文件 {file_path}: {e}")
    return content

def write_vm_file(file_path, vm_code: List[str]) -> None:
    """
    将 VM 代码写入指定路径的 .vm 文件

    参数:
        file_path (str): 目标 .vm 文件的路径
        vm_code (List[str]): VM 代码，按行分割，作为字符串列表

    返回: None
    """
    assert file_path.endswith('.vm'), f"文件必须是 .vm 格式，但得到 {file_path}"

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in vm_code:
                file.write(line + '\n')
    except Exception as e:
        raise IOError(f"无法写入文件 {file_path}: {e}")
