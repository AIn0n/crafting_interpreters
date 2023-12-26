#ifndef _RLE_H_
#define _RLE_H_

#include "common.h"
#include "memory.h"

/**
 *  things are stored as a array of pairs where the first element is value and the 
 * second one is length. For example array [99, 99, 21, 21, 21] will be compressed to
 * array [99, 2, 21, 3].
 */
typedef struct {
    size_t count;
    size_t capacity;
    int *vals;
} rle_table;

void init_rle_table(rle_table *t);
int get_val_by_idx(const rle_table *t, const int idx);
void add_to_rle(rle_table *t, const int val);
void free_rle_table(rle_table *table);

#endif
