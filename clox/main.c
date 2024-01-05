#include "common.h"
#include "chunk.h"
#include "debug.h"
#include "vm.h"

int
main(int argc, const char* argv[])
{
	initVM();
	Chunk chunk;
	init_chunk(&chunk);

	/* index to place in constant table where 1.2 will be stored */
	int constant_idx = add_constant(&chunk, 1.2);
	write_chunk(&chunk, OP_CONSTANT, 123);
	write_chunk(&chunk, constant_idx, 123);

	write_chunk(&chunk, OP_RETURN, 123);

	disassemble_chunk(&chunk, "test chunk");
	interpret(&chunk);
	freeVM();
	free_chunk(&chunk);
	return 0;
}