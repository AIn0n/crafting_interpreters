#ifndef _VALUE_H_
#define _VALUE_H_

#include "common.h"

typedef double Value;

typedef struct {
    int capacity;
    int count;
    Value *values;
} Value_array;

void init_val_array(Value_array *array);
void write_val_array(Value_array *array, Value value);
void free_val_array(Value_array *array);

#endif