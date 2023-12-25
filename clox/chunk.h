#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"

typedef enum {
    OP_CONSTANT,
    OP_RETURN
} Op_code;

typedef struct
{
    int count;
    int capacity;
    uint8_t *code;
    Value_array constants;
} Chunk;

void init_chunk(Chunk *chunk);
void write_chunk(Chunk *chunk, uint8_t byte);
int add_constant(Chunk* chunk, Value value);
void free_chunk(Chunk *chunk);

#endif