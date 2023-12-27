#include "stab_alloc.h"
#include<math.h>
#include<stdio.h>

Stab_data
init_stab(void)
{
	return (Stab_data) {.len = {0}, .mem = {0}};
}

static int
find_free_block(const uint16_t *len, const int size)
{
	int count = 0, res;
	for (int n = 0; n < NUM_BLOCKS; ++n) {
		if (!(len[n] & PICK_MASK)) {
			if (!count)
				res = n;
			count++;
			if (count == size)
				return res;
		} else {
			count = 0;
		}
	}
	return -1;
}

uint64_t
salloc(Stab_data *data, size_t size)
{
	int block_needed = ceil((size + 0.0) / BLOCK_SIZE);
	printf("--- needed blocks = %i\n", block_needed);

	const int addr = find_free_block(data->len, block_needed);

	data->len[addr] = PICK_MASK + block_needed;
	for (int n = 1; n < block_needed; ++n) {
		data->len[addr + n] = PICK_MASK;
	}


	printf("--- found free %i\n", addr);
	printf("--- picked addr %llu\n", (uint64_t) data->mem + addr * BLOCK_SIZE);
	return (uint64_t) data->mem + addr * BLOCK_SIZE;
}

static uint16_t
retrieve_block(const Stab_data *d, const uint64_t ptr)
{
	return (ptr - (uint64_t)d->mem) / BLOCK_SIZE;
}

static uint16_t
retrieve_size(const Stab_data *d, const uint16_t idx)
{
	return d->len[idx] - PICK_MASK;
}

void *
srealloc(Stab_data *d, void *ptr, size_t new_size)
{
	const uint64_t _ptr = (uint64_t) ptr;
	const uint16_t idx = retrieve_block(d, _ptr);
	const uint16_t size = retrieve_size(d, idx);
	if (new_size <= size * BLOCK_SIZE)
		return ptr;
	
	for (int n = idx + size; n < NUM_BLOCKS; ++n) {

	}

	return 0;
}

void
sfree(Stab_data *data, const void *ptr)
{
	const uint64_t addr = (uint64_t) ptr;
	uint16_t idx = retrieve_block(data, addr);
	printf("(free) found block = %i\n", idx);
	uint16_t size = retrieve_size(data, idx);
	printf("(free) block size = %i\n", size);
	for (uint16_t n = 0; n < size; ++n) {
		data->len[n + idx] = 0;
	}
}
