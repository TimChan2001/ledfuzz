def add_line_numbers(code: str, start_line: int) -> str:
    """
    给代码加上从 start_line 开始的行号
    """
    lines = code.strip().splitlines()
    numbered_lines = [f"{i+start_line} {line}" for i, line in enumerate(lines)]
    return "\n".join(numbered_lines)

if __name__ == "__main__":
    # 示例输入
    start_line = int(input("请输入起始行号："))
    print("请输入代码，输入END结束：")
    input_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        input_lines.append(line)

    code = "\n".join(input_lines)
    result = add_line_numbers(code, start_line)
    print("\n加上行号的代码：")
    print(result)
