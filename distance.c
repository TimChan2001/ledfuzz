#include "distance.h"
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/shm.h>

volatile uint8_t *trace_bits = NULL;

void setup_shm() {
    char *shm_env = getenv("__AFL_SHM_ID");
    if (shm_env) {
        int shm_id = atoi(shm_env);
        trace_bits = (uint8_t *) shmat(shm_id, NULL, 0);
        if (trace_bits == (void *) -1) {
            perror("shmat");
            exit(1);
        }
    }
}

void distance_instrument(int distance) {
    if (!trace_bits) {
        perror("Shm not set");
        abort();
    }
    int *shm_distance = (int *)(trace_bits + MAP_SIZE + 16);
    *shm_distance = distance;
    uint64_t *reach_tag = (uint64_t *)(trace_bits + MAP_SIZE + 24);
    *reach_tag = 1;
}
