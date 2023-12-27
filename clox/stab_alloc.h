#ifndef _STAB_ALLOC_H_
#define _STAB_ALLOC_H_

#include "common.h"

#define NUM_BLOCKS 20000
#define BLOCK_SIZE 255
/** This mask is based on assumption, that longest possible chain of blocks is 
*   15 bit length. Last bit is used to show which blocks are allocated.
*   32768 is most important bit in 16 bit unsigned int.
*/
#define PICK_MASK 32768

typedef struct {
    uint8_t mem[NUM_BLOCKS * BLOCK_SIZE];
    uint16_t len[NUM_BLOCKS];
}
Stab_data;


Stab_data init_stab(void);
uint64_t salloc(Stab_data *data, size_t size);
void sfree(Stab_data *data, const void *addr);

#endif
