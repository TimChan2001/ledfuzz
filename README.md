# ledfuzz
prototype for LEDFuzz

### llm-query usage
```
python3 /home/yiyang/ledfuzz/llm-query.py BugXXX/ outfile_name
```

BugXXX/ should be as follows:
```
BugXXX/
│── bug-report/ # Detailed bug report and analysis
│── name/ # Identifier or name-related information
└── source-code/ # Source code files relevant to the bug
```

### Fuzzing with LEDFuzz (Version cf5c7ab)

##### 1. Replace `afl-fuzz.c`
Replace `afl-fuzz.c` with the file of the same name in AFLGo (version `cf5c7ab`) to build the fuzzer.

##### 2. Insert Triggering Condition Monitor
Insert a **triggering condition monitor** into the target program and compile it:

```c
+ #include "distance.h"

+ distance_instrument(double distance, uint8_t save_index, uint8_t exec_sequence, uint8_t conjunct, double weight);
```

##### 3. Start Fuzzing
```
afl-fuzz -a [ins_num] -s [seq_num] ...
```

##### 4. Observe Terminal Output
Current maximum/minimum triggering distance:
```c
printf("max_t_d: %f  min_t_d: %f\n", max_triggering_distance, min_triggering_distance);
```
