#ifndef DISTANCE_H
#define DISTANCE_H

#include <stdint.h>

#define MAP_SIZE (1 << 16)

extern volatile uint8_t *trace_bits;

void distance_instrument(int distance);

#endif
