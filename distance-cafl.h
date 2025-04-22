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

/* 8x u8  8x u8  8x [double u8 u8 double] */

static void distance_instrument(double distance, uint8_t save_index, uint8_t exec_sequence, uint8_t conjunct, double weight) {
    char *shm_env = getenv("__AFL_SHM_ID");
    uint8_t *trace_bits = NULL;
    if (shm_env) {
        int shm_id = atoi(shm_env);
        trace_bits = (uint8_t *) shmat(shm_id, NULL, 0);
        if (!trace_bits) {
            perror("shmat");
            abort();
        }

        // sequence flag
        uint8_t *seq_save = trace_bits + MAP_SIZE + 32 + save_index * 18 + 8;
        *seq_save = exec_sequence;

        uint8_t *seq = trace_bits + MAP_SIZE + 24 + exec_sequence;
        *seq = 1;

        // reach flag
        uint8_t *reach_flag = trace_bits + MAP_SIZE + 16 + save_index;
        double *trig_distance = (double *)(trace_bits + MAP_SIZE + 32 + save_index * 18);
        if (!(*reach_flag) || distance < *trig_distance)
            *trig_distance = distance;
        *reach_flag = 1;

        // conjunct
        uint8_t *conjunct_save = trace_bits + MAP_SIZE + 32 + save_index * 18 + 8 + 1;
        *conjunct_save = conjunct;

        // weight
        double *weight_save = (double *)(trace_bits + MAP_SIZE + 32 + save_index * 18 + 8 + 1 + 1);
        *weight_save = weight;
    }
}

#endif /* DISTANCE_H */
