#include "distance.h"
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/shm.h>
#include <limits.h>

volatile uint8_t *trace_bits = NULL;

void distance_instrument(int distance) {
    char *shm_env = getenv("__AFL_SHM_ID");
    if (shm_env && !trace_bits) {
        int shm_id = atoi(shm_env);
        trace_bits = (uint8_t *) shmat(shm_id, NULL, 0);
        if (trace_bits == (void *) -1) {
            perror("shmat");
            exit(1);
        }
        int *shm_distance_orig = (int *)(trace_bits + MAP_SIZE + 16);
        *shm_distance_orig = INT_MAX;
        uint64_t *reach_tag_orig = (uint64_t *)(trace_bits + MAP_SIZE + 24);
        *reach_tag_orig = 0;
    }
    if (!trace_bits) {
        perror("Shm not set");
        abort();
    }
    int *shm_distance = (int *)(trace_bits + MAP_SIZE + 16);
    if (distance < *shm_distance)
        *shm_distance = distance;
    uint64_t *reach_tag = (uint64_t *)(trace_bits + MAP_SIZE + 24);
    *reach_tag = 1;
}
