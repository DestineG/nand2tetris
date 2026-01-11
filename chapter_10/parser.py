# chapter_10/parser.py

from chapter_10.utils.utils import remove_comments_and_whitespace
from chapter_10.Class import handle_class

def handleSingleJackFile(jack_path):
    with open(jack_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    pure_code_lines = remove_comments_and_whitespace(raw_lines)
    
    return pure_code_lines

def parser(jack_path, output_path):
    code_lines = handleSingleJackFile(jack_path)
    codeStr = ""
    for line in code_lines:
        codeStr += line + " "
    xml = handle_class(codeStr)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml)
    return xml

if __name__ == "__main__":
    jack_file_path = r"chapter_10\ArrayTest\Main.jack"
    output_file_path = r"chapter_10\ArrayTest\MainCustom.xml"
    parser(jack_file_path, output_file_path)