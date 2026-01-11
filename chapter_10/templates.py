# chapter_10/templates.py

from chapter_10.utils.utils import remove_comments_and_whitespace

def handleSingleJackFile(jack_path):
    with open(jack_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    pure_code_lines = remove_comments_and_whitespace(raw_lines)
    
    return pure_code_lines

jack_file_path = r"chapter_10\test.jack"
code_line = handleSingleJackFile(jack_file_path)
for line in code_line:
    print(line)