# chapter_10/utils/utils.py

def remove_comments_and_whitespace(lines):
    cleaned_lines = []
    in_block_comment = False

    for line in lines:
        i = 0
        result = ""
        in_string = False  # 字符串状态
        
        while i < len(line):
            # 1. 处理字符串状态开关 (只有在非注释状态下才生效)
            if not in_block_comment and line[i] == '"':
                in_string = not in_string
                result += line[i]
                i += 1
                continue

            # 2. 如果在字符串里，什么都不管，直接加字符
            if in_string:
                result += line[i]
                i += 1
                continue

            # 3. 处理块注释（只有在非字符串状态下才生效）
            if not in_block_comment and line[i:i+2] == "/*":
                in_block_comment = True
                i += 2
            elif in_block_comment and line[i:i+2] == "*/":
                in_block_comment = False
                i += 2
            # 4. 处理行注释
            elif not in_block_comment and line[i:i+2] == "//":
                break
            # 5. 正常的代码内容
            else:
                if not in_block_comment:
                    result += line[i]
                i += 1

        result = result.strip()
        if result:
            cleaned_lines.append(result)

    return cleaned_lines
