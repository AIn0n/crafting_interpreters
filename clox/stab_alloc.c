#include "stab_alloc.h"
#include<math.h>
#include<stdio.h>
#include<stdlib.h>

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

static int
ceil_blocks(const size_t size)
{
	return ceil((size + 0.0) / BLOCK_SIZE);
}

static int
floor_blocks(const size_t size)
{
	return size / BLOCK_SIZE;
}

static void
salloc_by_idx(Stab_data *d, const uint16_t idx, const size_t size)
{
	d->len[idx] = PICK_MASK + size;
	for (int n = 1; n < size; ++n)
		d->len[idx + n] = PICK_MASK;
}

void*
salloc(Stab_data *data, size_t size)
{
	const int block_needed = ceil_blocks(size);
	/**
	 * What would be good to do here, is to make some sort of partitioning,
	 * choosing spots for new allocated pointers somewhere in the middle of 
	 * longest continous free block. Right now I'm leaving this right here.
	 */
	const int addr = find_free_block(data->len, block_needed);
	salloc_by_idx(data, addr, block_needed);

	return data->mem + addr * BLOCK_SIZE;
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
	const uint16_t idx = retrieve_block(d, (uint64_t) ptr);
	const uint16_t size = retrieve_size(d, idx);
	const int diff = new_size - size * BLOCK_SIZE;

	// case where needed memory is less than we actually have
	if (diff < 0) {
		if (size == 1)
			return ptr;
		// free all blocks
		for (int n = 0; n < size; ++n)
			d->len[n + idx] = 0;
		// compute new size and realloc the blocks
		const int new_size = size - floor_blocks(abs(diff));
		salloc_by_idx(d, idx, new_size);
		return ptr;
	}

	const int diff_blocks = ceil_blocks(diff);

	int free_count = 0;
	// check if next block after current one are free
	for (int n = idx + size; n < NUM_BLOCKS; ++n) {
		if (d->len[n] & PICK_MASK)
			break;
		else if (++free_count == diff_blocks) {
			salloc_by_idx(d, idx, size + diff_blocks);
			return ptr;
		}
	}

	/** at this point we are sure that we looking for bigger address and nearby blocks
	 *  are already allocated
	 */
	sfree(d, ptr);
	return salloc(d, new_size);
}

void
sfree(Stab_data *data, const void *ptr)
{
	const uint64_t addr = (uint64_t) ptr;
	uint16_t idx = retrieve_block(data, addr);
	uint16_t size = retrieve_size(data, idx);
	for (uint16_t n = 0; n < size; ++n) {
		data->len[n + idx] = 0;
	}
}
