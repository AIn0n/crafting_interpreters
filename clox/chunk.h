#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"

typedef enum {
    OP_CONSTANT,
    OP_NEGATE,
    OP_NOT,
    OP_ADD,
    OP_NIL,
    OP_TRUE,
    OP_FALSE,
    OP_EQUAL,
    OP_GREATER,
    OP_LESS,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_RETURN,
} Op_code;

typedef struct
{
    int count;
    int capacity;
    uint8_t *code;
    int *lines;
    Value_array constants;
} Chunk;

void init_chunk(Chunk *chunk);
void write_chunk(Chunk *chunk, uint8_t byte, int line);
int add_constant(Chunk* chunk, Value value);
void free_chunk(Chunk *chunk);

#endif