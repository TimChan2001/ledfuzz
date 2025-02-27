# ledfuzz
prototype for LEDFuzz

### llm-query usage
```
python3 /home/yiyang/ledfuzz/llm-query.py
> BugXXX/
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

+ setup_shm();
+ distance_instrument(int distance);
```

##### 3. Perform Fuzzing and Observe Terminal Output
Current maximum/minimum triggering distance:
```
printf("max_t_d: %f  min_t_d: %f\n", max_triggering_distance, min_triggering_distance);
```

Current triggering distance corresponding power factor:
```
printf("power_factor_t: %f\n", power_factor_t);
```
