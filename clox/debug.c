#include<stdio.h>

#include "debug.h"
#include "value.h"

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

	if (offset > 0 && chunk->lines[offset] == chunk->lines[offset - 1]) {
		printf("   | ");
	} else {
		printf("%4d ", chunk->lines[offset]);
	}

	uint8_t instruction = chunk->code[offset];
	switch (instruction) {
	case OP_CONSTANT:
		return constant_instruction("OP_CONSTANT", chunk, offset);
	case OP_NEGATE:
		return simple_instruction("OP_NEGATE", offset);
	case OP_ADD:
		return simple_instruction("OP_ADD", offset);
	case OP_SUB:
		return simple_instruction("OP_SUB", offset);
	case OP_MUL:
		return simple_instruction("OP_MUL", offset);
	case OP_DIV:
		return simple_instruction("OP_DIV", offset);
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