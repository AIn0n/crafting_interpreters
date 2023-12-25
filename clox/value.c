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
	printf("%g", val);
}