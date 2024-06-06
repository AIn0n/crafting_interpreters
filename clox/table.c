#include <stdlib.h>
#include <string.h>

#include "memory.h"
#include "object.h"
#include "table.h"
#include "value.h"

#define TABLE_MAX_LOAD 0.75

void
init_table(Table *table)
{
	table->count = 0;
	table->capacity = 0;
	table->entries = NULL;
}

void
free_table(Table *table)
{
	FREE_ARRAY(Entry, table->entries, table->capacity);
	init_table(table);
}

static Entry*
find_entry(Entry *entries, int capacity, ObjString *key)
{
	uint32_t index = key->hash % capacity;
	for (;;) {
		Entry *entry = &entries[index];
		if (entry->key == key || entry->key == NULL)
			return entry;
		index = (index + 1) % capacity;
	}
}

bool
table_set(Table *table, ObjString *key, Value value)
{
	if (table->count + 1 > table->capacity * TABLE_MAX_LOAD) {
		int capacity = GROW_CAPACITY(table->capacity);
		adjust_capacity(table, capacity);
	}
	Entry *entry = find_entry(table->entries, table->capacity, key);
	bool is_new_key = (entry->key == NULL);
	if (is_new_key)
		table->count++;
	
	entry->key = key;
	entry->value = value;
	return is_new_key;
}
