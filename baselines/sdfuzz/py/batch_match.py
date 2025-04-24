import os
import sys
import subprocess

def generate_and_run_shell_script(input_dir, fixed_input_file, output_dir, shell_script_path="run_match.sh"):
    lines = []

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if os.path.isfile(file_path):
            output_path = os.path.join(output_dir, filename)
            line = f"python3 py/match_log.py {file_path} {fixed_input_file} > {output_path}"
            lines.append(line)

    with open(shell_script_path, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n\n")
        f.write("\n".join(lines) + "\n")

    print(f"[✔] Shell 脚本已生成: {shell_script_path}，共 {len(lines)} 条命令")

    # 添加执行权限
    subprocess.run(["chmod", "+x", shell_script_path])
    print(f"[✔] 设置执行权限: chmod +x {shell_script_path}")

    # 运行脚本
    print(f"[▶] 正在执行脚本: {shell_script_path} ...")
    subprocess.run(["bash", shell_script_path])
    print(f"[✔] 执行完成")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python3 batch_match.py <log文件夹> <函数列表文件> <输出文件夹>")
        sys.exit(1)

    input_dir = sys.argv[1]
    fixed_input_file = sys.argv[2]
    output_dir = sys.argv[3]

    generate_and_run_shell_script(input_dir, fixed_input_file, output_dir)
