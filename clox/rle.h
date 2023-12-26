#ifndef _RLE_H_
#define _RLE_H_

#include "common.h"
#include "memory.h"

/**
 *  things are stored as a array of pairs where the first element is value and the 
 * second one is lenght. For example array [99, 99, 21, 21, 21] will be compressed to
 * array [99, 2, 21, 3].
 */
typedef struct {
    size_t count;
    size_t capacity;
    int *vals;
} rle_table;

/**
 *  rle table starts filled with the capacity for 8 elements.
 *  This make logic of growing a bit simpler, probably more optimized.
 */
rle_table
init_rle_table(void)
{
    rle_table t = {.count = 0, .capacity = 8, .vals = NULL};
    GROW_ARRAY(int, t.vals, 0, 8);
    return t;
}

/**
 *  Return value from rle based on index. So, if you created rle based upon array 
 *  of five elements equal to [0, 1, 2, 7, 7], and you want third index you will get <7>.
 */
int
get_val_by_idx(const rle_table *t, const int idx)
{
    int n = 1, counter = 0;
    do {
        counter += t->vals[n];
        n += 2;
    }
    while (counter < idx && counter < t->count);
    return t->vals[n - 3];
}

void
add_to_rle(rle_table *t, int val)
{
    if (val == t->vals[t->count - 2]) {
        t->vals[t->count - 1]++;
    } else {
        if (t->capacity < t->count + 2) {
            int old_cap = t->capacity;
            t->capacity *= 2;
            t->vals = GROW_ARRAY(int, t->vals, old_cap, t->capacity);
        }
        t->count += 2;
        t->vals[t->count - 1] = 1;
        t->vals[t->count - 2] = val;
    }
}

#endif