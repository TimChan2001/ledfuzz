# Baseline: SDFuzz

### Usage

1. **Replace the AFL LLVM pass**
    Replace `afl-llvm-pass.so.cc` (in `afl-2.52b`) with `trace_afl-llvm-pass.so.cc`, then recompile `afl-clang-fast` and `afl-clang-fast++`.

2. **Compile the target program**
    Use the newly compiled `afl-clang-fast` or `afl-clang-fast++` to compile your target program.
    During runtime, the instrumented binary will output a **function call log** — redirect it to a file using `>`.

3. **Extract target call trace**
   Extract the **call trace** from asan log of the target vulnerability using the provided scripts.

   ```shell
   python3 py/parser.py /path/to/asan.log] [/path/to/output]
   ```

4. **Run the analysis script**
    Use the script to analyze the log and **identify irrelevant functions**

   ```shell
   anaylze_irrel_funcs.sh [/path/to/sdfuzz] [/path/to/trace_logs_dir] [/path/to/target_trace_file] [/path/to/match_results_dir] [/path/to/output_dir]
   ```

   Check functions_to_cull.json in /path/to/output_dir