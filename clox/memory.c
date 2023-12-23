#include "memory.h"

void*
reallocate(void* pointer, size_t old_size, size_t new_size)
{
	if (!new_size) {
		free(pointer);
		return NULL;
	}
	void* result = realloc(pointer, new_size);
	if (!result)
		exit(1);
	return result
}