import sys
import re

log_lines = []

def extract_func(line):
    """ 提取函数名和类型（TRACE/CALL） """
    if "[TRACE]" in line:
        match = re.search(r'Function (\w+)', line)
        return match.group(1) if match else None, "TRACE"
    elif "[CALL]" in line:
        match = re.search(r'Entering function: (\w+)', line)
        return match.group(1) if match else None, "CALL"
    return None, None

def find_last_match(target_funcs):
    """ 从尾到头找最后一次完整匹配 """
    reversed_targets = target_funcs[::-1]
    matched_funcs = []
    target_index = 0
    i = len(log_lines) - 1

    while i >= 0:
        line = log_lines[i]
        func_name, kind = extract_func(line)

        if func_name and func_name == reversed_targets[target_index]:
            # 优先取 TRACE，如果当前是 CALL，上一行是对应 TRACE，则用上一行
            if kind == "CALL" and i > 0:
                prev_func, prev_kind = extract_func(log_lines[i - 1])
                if prev_kind == "TRACE" and prev_func == func_name:
                    matched_funcs.append((func_name, i))  # 使用 TRACE 行
                    i -= 1  # 跳过上面的 TRACE
                else:
                    matched_funcs.append((func_name, i + 1))
            else:
                matched_funcs.append((func_name, i + 1))

            target_index += 1
            if target_index == len(reversed_targets):
                break
        i -= 1

    if target_index == len(reversed_targets):
        return True, matched_funcs[::-1]
    else:
        return False, matched_funcs[::-1]

def find_longest_prefix_subsequence(target_funcs):
    """ 从头开始找最长前缀子序列 """
    longest = []
    current_index = 0

    for line in log_lines:
        func_name, _ = extract_func(line)
        if func_name and func_name == target_funcs[current_index]:
            longest.append(func_name)
            current_index += 1
            if current_index == len(target_funcs):
                break

    return longest

def parse_log_and_match_last(log_file: str, trace_file: str):
    # 加载输入
    with open(trace_file, 'r', encoding='utf-8') as f:
        target_funcs = f.read().strip().split(',')

    with open(log_file, 'r', encoding='utf-8') as f:
        global log_lines
        log_lines = f.readlines()

    # 尝试完整匹配
    success, matches = find_last_match(target_funcs)
    if success:
        return True, matches

    # 匹配失败，找最长子串并匹配其最晚出现
    longest_subseq = find_longest_prefix_subsequence(target_funcs)
    if longest_subseq:
        success, matches = find_last_match(longest_subseq)
        return False, matches
    else:
        return False, []

# 命令行调用
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python match_log.py <log文件> <函数列表文件>")
        sys.exit(1)

    log_file = sys.argv[1]
    func_file = sys.argv[2]
    success, matches = parse_log_and_match_last(log_file, func_file)

    print("Matched full sequence!\n" if success else "Partial match (longest subsequence):\n")
    for func, line_no in matches:
        print(f"[{line_no}] {log_lines[line_no-1]}", end='')
