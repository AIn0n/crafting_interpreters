#include <stdio.h>

#include "common.h"
#include "debug.h"
#include "vm.h"
#include "memory.h"

VM vm;

static void
reset_stack()
{
	vm.stack.cap = 0;
	vm.stack.count = 0;
	vm.stack.vals = NULL;
}

void
initVM() 
{
	reset_stack();
}

void
freeVM()
{
	FREE_ARRAY(Value, vm.stack.vals, vm.stack.cap);
}

void
push(Value val)
{
	if (vm.stack.cap < vm.stack.count + 1) {
		int old_cap = vm.stack.cap;
		vm.stack.cap = GROW_CAPACITY(old_cap);
		vm.stack.vals = GROW_ARRAY(Value, vm.stack.vals, old_cap, vm.stack.cap);
	}
	vm.stack.vals[vm.stack.count++] = val;
}

Value
pop(void)
{
	return vm.stack.vals[--vm.stack.count];
}

static Interpret_res
run()
{
#define READ_BYTE() (*vm.ip++)
#define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])
#define BINARY_OP(op)			\
	do {				\
		double b = pop();	\
		double a = pop();	\
		push(a op b);		\
	} while (false);

	for (;;) {
#ifdef DEBUG_TRACE_EXECUTION
		/* stack printing segment of the code */
		printf("          ");
		for (int i = 0; i < vm.stack.count; ++i) {
			printf("[ ");
			print_val(vm.stack.vals[i]);
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
		case OP_NEGATE:
			push(-pop());
			break;
		case OP_ADD:
			BINARY_OP(+);
			break;
		case OP_SUB:
			BINARY_OP(-);
			break;
		case OP_MUL:
			BINARY_OP(*);
			break;
		case OP_DIV:
			BINARY_OP(/);
			break;
		case OP_RETURN:
			print_val(pop());
			puts("");
			return INTERPRET_OK;
		}
	}

#undef READ_BYTE
#undef READ_CONSTANT
#undef BINARY_OP
}

Interpret_res interpret(Chunk* chunk)
{
	vm.chunk = chunk;
	vm.ip = vm.chunk->code;
	return run();
}
