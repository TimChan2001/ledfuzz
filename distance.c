#include "distance.h"
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/shm.h>

volatile uint8_t *trace_bits = NULL; // AFL 共享内存指针

// 连接 AFL 共享内存
void setup_shm() {
    char *shm_env = getenv("AFL_SHM_ID");
    if (shm_env) {
        int shm_id = atoi(shm_env);
        trace_bits = (uint8_t *) shmat(shm_id, NULL, 0);
        if (trace_bits == (void *) -1) {
            perror("shmat");
            exit(1);
        }
    }
}

// 存储 distance 到 AFL 共享内存
void distance_instrument(int distance) {
    if (!trace_bits) return; // 确保共享内存已连接

    uint64_t *shm_distance = (uint64_t *)(trace_bits + MAP_SIZE);
    *shm_distance = (uint64_t) abs(distance);  // 取绝对值，避免负数影响计算
}
