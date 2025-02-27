#!/bin/bash
# 自动调用执行llm_query.py

# 设置目标范围
# 两种方式选其一，设置taget_ids或设置[START,END]，需要相应修改line 22/23的循环
PROGRAM_NAME="tiff"
# target_ids =(4 6 7 8 9 10 12 14)
target_ids =(8 12)
START=2
END=14

# 输出文件名，不需要路径
OUT_FILE="out4"

# 日志文件路径
LOG_FILE="query_log.log"

# 清空日志文件，开始新的日志记录
> $LOG_FILE

# 循环执行命令
for i in "${my_list[@]}"; do
#for i in $(seq $START $END); do
    TARGET="$PROGRAM_NAME-$i"
    START_TIME=$(date +%s)

    # 写入日志文件，执行命令并捕获输出和错误信息
    # stderr重定向到stdout，进而被写入日志文件
    echo "Executing: python llm-query.py /home/gnq/llm_dirfuzz/ledfuzz/targets/$TARGET $OUT_FILE" >> $LOG_FILE
    python llm-query.py /home/gnq/llm_dirfuzz/ledfuzz/targets/$TARGET $OUT_FILE >> $LOG_FILE 2>&1
    
    # 检查命令是否成功执行，失败时记录错误信息
    if [ $? -ne 0 ]; then
        echo "Error: Command for $TARGET failed!" >> $LOG_FILE
    else
        echo "Success: Command for $TARGET executed successfully." >> $LOG_FILE
    fi

    END_TIME=$(date +%s)

    # 计算执行时长（秒）
    EXECUTION_TIME=$((END_TIME - START_TIME))

    echo "Execution time for $TARGET: ${EXECUTION_TIME} seconds" >> $LOG_FILE
done