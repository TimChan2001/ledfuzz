#!/bin/bash

# 参数检查
if [ "$#" -ne 5 ]; then
    echo "用法: $0 [prefix_path] [trace_logs_dir] [target_trace_file] [match_results_dir] [output_dir]"
    exit 1
fi

# 参数解析
PREFIX_PATH=$1
TRACE_LOGS_DIR=$2
TARGET_TRACE_FILE=$3
MATCH_RESULTS_DIR=$4
OUTPUT_DIR=$5

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 输出文件路径
RELEVANT_FUNCS_JSON="$OUTPUT_DIR/functions_relevant.json"
TO_CULL_FUNCS_JSON="$OUTPUT_DIR/functions_to_cull.json"

# 执行 batch_match.py
echo "🚀 Running batch_match.py..."
python3 "$PREFIX_PATH/py/batch_match.py" "$TRACE_LOGS_DIR" "$TARGET_TRACE_FILE" "$MATCH_RESULTS_DIR"

# 执行 analyze_funcs.py
echo "🔍 Running analyze_funcs.py..."
python3 "$PREFIX_PATH/py/analyze_funcs.py" "$MATCH_RESULTS_DIR" "$TRACE_LOGS_DIR" "$RELEVANT_FUNCS_JSON" "$TO_CULL_FUNCS_JSON"

echo "✅ 分析完成"
echo "Relevant functions saved to: $RELEVANT_FUNCS_JSON"
echo "Irrelevant (to cull) functions saved to: $TO_CULL_FUNCS_JSON"
