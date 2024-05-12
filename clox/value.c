#include <stdio.h>

#include "memory.h"
#include "value.h"

void
init_val_array(Value_array *array)
{
	array->values = NULL;
	array->capacity = 0;
	array->count = 0;
}

void
write_val_array(Value_array *array, Value value)
{
	if (array->capacity < array->count + 1) {
		int old_cap = array->capacity;
		array->capacity = GROW_CAPACITY(old_cap);
		array->values = GROW_ARRAY(
			Value,
			array->values,
			old_cap,
			array->capacity
		);
	}
	array->values[array->count] = value;
	array->count++;
}

void
free_val_array(Value_array *array)
{
	FREE_ARRAY(Value, array->values, array->capacity);
	init_val_array(array);
}

void
print_val(Value val)
{
	switch(val.type) {
	case VAL_BOOL:
		printf(AS_BOOL(val) ? "true" : "false");
		break;

	case VAL_NIL:	printf("nil"); 			break;
	case VAL_NUMBER:printf("%g", AS_NUMBER(val));	break;
	}
}

bool
valuesEqual(Value a, Value b)
{
	if (a.type != b.type) return false;
	switch(a.type) {
	case VAL_BOOL:
		return AS_BOOL(a) == AS_BOOL(b);
	case VAL_NIL:
		return true;
	case VAL_NUMBER:
		return AS_NUMBER(a) == AS_NUMBER(b);
	}
	return false;
}