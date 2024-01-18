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
#define BINARY_OP(op)			\
	do {				\
		double b = pop();	\
		double a = pop();	\
		push(a op b);		\
	} while (false);

	for (;;) {
		uint8_t instruction;
		switch (instruction = READ_BYTE()) {
		case OP_CONSTANT: {
			Value constant = READ_CONSTANT();
			push(constant);
			break;
		}
		case OP_NEGATE:
			*(vm.stack_top - 1) = - *(vm.stack_top - 1);
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
