#ifndef clox_vm_h_
#define clox_vm_h_

#include "chunk.h"
#include "value.h"


#define STACK_MAX 256

typedef struct {
    Chunk *chunk;
    uint8_t *ip;
    Value stack[STACK_MAX];
    Value *stack_top;
    Obj *objects;
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR,
} Interpret_res;

extern VM vm;

void initVM();
void freeVM();
Interpret_res interpret(const char *src);
void push(Value);
Value pop();

#endif