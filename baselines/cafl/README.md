# Baseline: CAFL

### Usage

1. stack/heap-buffer-overflow

   ```c
   + #include "distance-cafl.h"
   
   + distance_instrument_cafl(0.0+buf_len,0,0,0,1); // where the buffer was allocated
   ...
   + distance_instrument_cafl(0.0-read/write_index,1,1,0,1); // where the bof occurred
   ```

2. use-after-free, double-free, and use-of-uninitialized-value

   ```c
   + #include "distance-cafl.h"
   
   + distance_instrument_cafl(0.0,0,0,0,1); // free in uaf, 1st free in df, use in ubi
   ...
   + distance_instrument_cafl(0.0,1,1,0,1); // use in uaf, 2nd free in df, initialize in ubi
   ```

3. assertion-failure and divide-by-zero

   ```c
   + #include "distance-cafl.h"
   
   + distance_instrument_cafl(0.0+abs(denominator),0,0,0,1); // divide-by-zero
   or
   + distance_instrument_cafl(0.0+condition,0,0,0,1); // assertion-failure
   ```

   

Start fuzzing with afl-fuzz (ver. afl-fuzz-cafl.c).