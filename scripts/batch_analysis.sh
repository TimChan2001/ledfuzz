#!/bin/bash
# 批量分析文件夹下所有monitor文件夹中的内容,并写入文件
# example: ./batch_analysis.sh /home/gnq/llm_dirfuzz/magma/tools/captain/workdir-afl results-afl.txt

# 输入文件和输出文件配置
input_file="./monitor_paths.txt"   # 存放路径列表的文件
input_dir=$1
output_file=$2 # 结果输出文件

if [[ -z "$input_dir" || -z "$output_file" ]]; then
    echo "Usage: $0 <input_directory> <output_file>"
    exit 1
fi

find "$input_dir" -type d -name "monitor" -print > $input_file
# 清空已存在的输出文件
> "$output_file"

# 逐行读取路径并处理
while IFS= read -r path; do
    # 跳过空行
    [[ -z "$path" ]] && continue
    
    # 输出当前处理的路径到终端（可选）
    echo "Processing: $path"
    
    # 将路径和Python输出记录到结果文件
    echo "=== Path: $path ===" >> "$output_file"
    time python /home/gnq/llm_dirfuzz/ledfuzz/scripts/analysis.py "$path" >> "$output_file" 2>&1
    echo "" >> "$output_file"  # 添加空行分隔不同结果
    
done < "$input_file"

echo "All tasks completed. Results saved to $output_file"