#ifndef _VALUE_H_
#define _VALUE_H_

#include "common.h"

typedef enum {
    VAL_BOOL,
    VAL_NIL,
    VAL_NUMBER
} ValueType;

typedef struct {
    ValueType type;
    union {
        bool boolean;
        double number;
    } as;
} Value;

typedef struct {
    int capacity;
    int count;
    Value *values;
} Value_array;

void init_val_array(Value_array *array);
void write_val_array(Value_array *array, Value value);
void free_val_array(Value_array *array);

void print_val(Value val);

#endif