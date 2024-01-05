#ifndef clox_vm_h_
#define clox_vm_h_

#include "chunk.h"

typedef struct {
    Chunk *chunk;
    uint8_t *ip;
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR,
} Interpret_res;

void initVM();
void freeVM();
Interpret_res interpret(Chunk*);


#endif