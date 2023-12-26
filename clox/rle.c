#include "rle.h"

/**
 *  rle table starts filled with the capacity for 8 elements.
 *  This make logic of growing a bit simpler, probably more optimized.
 */
void
init_rle_table(rle_table *t)
{
	t->count = 0;
	t->capacity = 8;
	t->vals = GROW_ARRAY(int, NULL, 0, 8);
}

/**
 *  Return value from rle based on index. So, if you created rle based upon array 
 *  of five elements equal to [0, 1, 2, 7, 7], and you want third index you will get <7>.
 */
int
get_val_by_idx(const rle_table *t, const int idx)
{
	int n = 1;
	for (int i = t->vals[1]; i <= idx; i += t->vals[n]) {
		n += 2;
	}
	return t->vals[n - 1];
}

void
add_to_rle(rle_table *t, int val)
{
	if (t->count && val == t->vals[t->count - 2]) {
		t->vals[t->count - 1]++;
		return;
	}
	
	if (t->capacity < t->count + 2) {
		
		int old_cap = t->capacity;
		t->capacity *= 2;
		t->vals = GROW_ARRAY(int, t->vals, old_cap, t->capacity);
	}
	t->vals[t->count] = val;
	t->count += 2;
	t->vals[t->count - 1] = 1;
}

void
free_rle_table(rle_table *table)
{
	FREE_ARRAY(int, table->vals, table->count);
}
