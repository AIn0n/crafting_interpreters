#ifndef clox_vm_h_
#define clox_vm_h_

#include "chunk.h"
#include "value.h"


#define STACK_MAX 256

typedef struct {
    Value *vals;
    int count;
    int cap;
} Stack;

typedef struct {
    Chunk *chunk;
    uint8_t *ip;
    Stack stack;
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR,
} Interpret_res;

void initVM();
void freeVM();
Interpret_res interpret(Chunk*);
void push(Value);
Value pop();

#endif