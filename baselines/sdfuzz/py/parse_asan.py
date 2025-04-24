import re
import sys

def parse_asan_trace_file(input_file: str, output_file: str):
    exclude_funcs = {"_start", "__libc_start_main"}
    function_names = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                match = re.search(r'in (\w+)', line)
                if match:
                    func = match.group(1)
                    if func not in exclude_funcs:
                        if func.startswith("MAGMA_"):
                            func = func[len("MAGMA_"):]
                        function_names.append(func)

    # 调用栈逆序（最底层的先输出）
    function_names.reverse()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(",".join(function_names))

# 命令行用法
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python parser.py <输入文件> <输出文件>")
    else:
        parse_asan_trace_file(sys.argv[1], sys.argv[2])
