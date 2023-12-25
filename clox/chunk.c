#include "chunk.h"
#include "memory.h"

void
init_chunk(Chunk *chunk)
{
	chunk->capacity = 0;
	chunk->count = 0;
	chunk->code = NULL;
	init_val_array(&chunk->constants);
}

void
write_chunk(Chunk* chunk, uint8_t byte)
{
	if (chunk->capacity < chunk->count + 1) {
		int old_cap = chunk->capacity;
		chunk->capacity = GROW_CAPACITY(old_cap);
		chunk->code = GROW_ARRAY(uint8_t, chunk->code, old_cap, chunk->capacity);
	}
	chunk->code[chunk->count] = byte;
	chunk->count++;
}

int
add_constant(Chunk* chunk, Value value)
{
	write_val_array(&chunk->constants, value);
	return chunk->count - 1;
}

void
free_chunk(Chunk *chunk)
{
	FREE_ARRAY(uint8_t, chunk->code, chunk->capacity);
	free_val_array(&chunk->constants);
	init_chunk(chunk);
}