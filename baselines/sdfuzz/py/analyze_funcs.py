import os
import re
import json
import sys

def extract_func_from_line(line):
    """从一行中提取函数名"""
    if "[TRACE]" in line:
        match = re.search(r'Function (\w+)', line)
        return match.group(1) if match else None
    elif "[CALL]" in line:
        match = re.search(r'Entering function: (\w+)', line)
        return match.group(1) if match else None
    return None

def print_progress(current, total, bar_length=40):
    percent = current / total
    filled_len = int(round(bar_length * percent))
    bar = '█' * filled_len + '-' * (bar_length - filled_len)
    print(f"\rProgress: |{bar}| {current}/{total} files", end='', flush=True)

def analyze_matched_logs(result_dir, log_dir):
    seen_funcs_in_matched = set()
    all_funcs_in_logs = set()
    files = [f for f in os.listdir(result_dir) if os.path.isfile(os.path.join(result_dir, f))]
    total = len(files)

    for idx, filename in enumerate(files, start=1):
        result_path = os.path.join(result_dir, filename)
        if not os.path.isfile(result_path):
            continue

        with open(result_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 尝试获取最后匹配行号
        last_line = None
        if lines and lines[0].startswith("Matched full sequence!"):
            for line in reversed(lines):
                match = re.match(r'\[(\d+)\]\s+\[.*?\]', line)
                if match:
                    last_line = int(match.group(1))
                    break

        # 打开 log 文件，获取所有函数（不论是否匹配）
        log_path = os.path.join(log_dir, filename)
        if not os.path.isfile(log_path):
            print(f"\n⚠️ 警告：未找到对应 log 文件 {log_path}")
            print_progress(idx, total)
            continue

        with open(log_path, 'r', encoding='utf-8') as log_f:
            log_lines = log_f.readlines()

        for i, line in enumerate(log_lines):
            func = extract_func_from_line(line)
            if func:
                all_funcs_in_logs.add(func)

            if last_line and i < last_line - 1 and func:
                seen_funcs_in_matched.add(func)

        print_progress(idx, total)

    print()  # 换行
    return seen_funcs_in_matched, all_funcs_in_logs

# 命令行使用方式
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python analyze_funcs.py <结果文件夹> <原始log文件夹> <输出文件A> <输出文件B>")
        print("输出文件A：匹配成功文件中使用过的函数集合")
        print("输出文件B：所有函数中未出现在集合A中的集合")
        sys.exit(1)

    result_dir = sys.argv[1]
    log_dir = sys.argv[2]
    output_file_A = sys.argv[3]
    output_file_B = sys.argv[4]

    funcs_A, funcs_all = analyze_matched_logs(result_dir, log_dir)
    funcs_B_minus_A = funcs_all - funcs_A

    with open(output_file_A, "w", encoding="utf-8") as f:
        json.dump(sorted(funcs_A), f, indent=2, ensure_ascii=False)

    with open(output_file_B, "w", encoding="utf-8") as f:
        json.dump(sorted(funcs_B_minus_A), f, indent=2, ensure_ascii=False)

    print(f"✅ 已保存集合A（已使用函数）至：{output_file_A}，共 {len(funcs_A)} 个函数")
    print(f"✅ 已保存集合B-A（未用函数）至：{output_file_B}，共 {len(funcs_B_minus_A)} 个函数")
