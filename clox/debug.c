#include<stdio.h>

#include "debug.h"
#include "value.h"
#include "rle.h"

static int
simple_instruction(const char *name, int offset)
{
	printf("%s\n", name);
	return offset + 1;
}

static int
constant_instruction(const char *name, Chunk *chunk, int offset)
{
	uint8_t constant = chunk->code[offset + 1];
	printf("%-16s %4d '", name, constant);
	print_val(chunk->constants.values[constant]);
	puts("'");
	return offset + 2;
}

int
disassemble_instr(Chunk *chunk, int offset)
{
	printf("%04d ", offset);

	int line = get_val_by_idx(&chunk->lines, offset);

	printf("%4d ", line);

	uint8_t instruction = chunk->code[offset];
	switch (instruction) {
	case OP_CONSTANT:
		return constant_instruction("OP_CONSTANT", chunk, offset);
	case OP_RETURN:
		return simple_instruction("OP_RETURN", offset);
	}
	printf("Unknown opcode %d", instruction);
	return offset + 1;
}

void
disassemble_chunk(Chunk *chunk, const char *name)
{
	printf("=== %s ===\n", name);
	for (int offset = 0; offset < chunk->count;) {
		offset = disassemble_instr(chunk, offset);
	}
}