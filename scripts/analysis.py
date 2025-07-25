# 分析monitor结果 
# python analysis.py <monitor_folder>
import os
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python analysis.py <monitor_folder>")
        return

    folder = sys.argv[1]

    # 收集并排序文件
    files = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue
        
        # 提取文件名中的数字部分
        name_part = os.path.splitext(filename)[0]
        try:
            num = int(name_part)
            files.append((num, filename))
        except ValueError:
            continue

    # 按数字升序排序
    files.sort(key=lambda x: x[0])

    targets = []
    counts = {}
    first_non_zero = {}

    for num, filename in files:
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'r') as f:
                lines = [line.strip() for line in f.readlines()[:2]]
                
                if len(lines) < 2:
                    print(f"警告：文件 {filename} 不足两行，已跳过")
                    continue
                
                names = lines[0].split(',')
                values = lines[1].split(',')
                
                if len(names) != len(values):
                    print(f"警告：文件 {filename} 两行长度不一致，已跳过")
                    continue
                
                #序号为1的文件为空，但是names仍然有，排除这种情况
                if names[0] == '':
                    continue

                for name, value_str in zip(names, values):
                    # 处理数值转换
                    try:
                        value = int(value_str)
                    except ValueError:
                        value = 0
                    
                    if name not in targets:
                        targets.append(name)
                        first_non_zero[name] = None
                    
                    # 统计出现次数
                    counts[name] = value
                    
                    # 检查并记录首次非零文件
                    if first_non_zero[name] is None and value != 0:
                        first_non_zero[name] = filename
        except Exception as e:
            print(f"处理文件 {filename} 时发生错误: {str(e)}")
            continue

    # 输出结果
    # print("\n统计数量:")
    # for target in targets:
    #     print(f"{target}: {counts[target]}")

    # print("\n首次出现非零值的文件:")
    for target in targets:
        result = first_non_zero[target] if first_non_zero[target] else "none"
        print(f"{target}: {result}")

    # 将结果写入文件
    # with open('result.txt', 'w') as f:
    #     for target in targets:
    #         result = first_non_zero[target] if first_non_zero[target] else "None"
    #         f.write(f"{target}: {result}\n")

if __name__ == '__main__':
    main()