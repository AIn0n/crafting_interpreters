#include <stdio.h>

#include "common.h"
#include "debug.h"
#include "vm.h"

VM vm;

static void
reset_stack()
{
	vm.stack_top = vm.stack;
}

void
initVM() 
{
	reset_stack();
}

void freeVM() {}

void
push(Value val)
{
	*vm.stack_top = val;
	vm.stack_top++;
}

Value
pop(void)
{
	vm.stack_top--;
	return *vm.stack_top;
}

static Interpret_res
run()
{
#define READ_BYTE() (*vm.ip++)
#define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])

	for (;;) {
#ifdef DEBUG_TRACE_EXECUTION
		/* stack printing segment of the code */
		printf("          ");
		for (Value* slot = vm.stack; slot < vm.stack_top; slot++) {
			printf("[ ");
			print_val(*slot);
			printf(" ]");
		}
		puts("");

		/* dissasembling every single instruction */
		disassemble_instr(vm.chunk, (int)(vm.ip - vm.chunk->code));
#endif
		uint8_t instruction;
		switch (instruction = READ_BYTE()) {
		case OP_CONSTANT: {
			Value constant = READ_CONSTANT();
			push(constant);
			break;
		}
		case OP_RETURN:
			print_val(pop());
			puts("");
			return INTERPRET_OK;
		}
	}

#undef READ_BYTE
#undef READ_CONSTANT
}

Interpret_res interpret(Chunk* chunk)
{
	vm.chunk = chunk;
	vm.ip = vm.chunk->code;
	return run();
}
