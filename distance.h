#ifndef DISTANCE_H
#define DISTANCE_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/shm.h>
#include <limits.h>

#define MAP_SIZE (1 << 16)

volatile uint8_t *trace_bits = NULL;

void distance_instrument(int distance) {
    FILE *file = fopen("/magma_out/output.txt", "a");
    char *shm_env = getenv("__AFL_SHM_ID");
    if (shm_env) {
        int shm_id = atoi(shm_env);
        trace_bits = (uint8_t *) shmat(shm_id, NULL, 0);
        if (!trace_bits) {
            perror("shmat");
            abort();
        }
        uint64_t *reach_tag = (uint64_t *)(trace_bits + MAP_SIZE + 24);
        int *shm_distance = (int *)(trace_bits + MAP_SIZE + 16);
        fprintf(file, "orig_1: %d\n",*shm_distance);
        fprintf(file, "rt: %d\n",*reach_tag);
        if (!(*reach_tag) || distance < *shm_distance)
            *shm_distance = distance;
        *reach_tag = 217;
        fprintf(file, "update: %d\n",distance);
        fprintf(file, "orig_2: %d\n\n",*shm_distance);
    }
    fclose(file);
}

#endif /* DISTANCE_H */
