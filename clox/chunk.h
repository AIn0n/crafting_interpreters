#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"
#include "rle.h"

#define CONST_IDX_BYTES 3

typedef enum {
    OP_CONSTANT,
    OP_CONSTANT_LONG,
    OP_RETURN
} Op_code;

typedef struct
{
    int count;
    int capacity;
    uint8_t *code;
    rle_table lines;
    Value_array constants;
} Chunk;

void init_chunk(Chunk *chunk);
void write_chunk(Chunk *chunk, uint8_t byte, int line);
int add_constant(Chunk* chunk, Value value);
void free_chunk(Chunk *chunk);

void write_constant(Chunk *chunk, const Value value, const int line);

#endif
