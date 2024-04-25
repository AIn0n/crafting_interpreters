#include <stdarg.h>
#include <stdio.h>

#include "common.h"
#include "debug.h"
#include "vm.h"
#include "compiler.h"

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

static void
runtime_error(const char *format, ...)
{
	va_list args;
	va_start(args, format);
	vfprintf(stderr, format, args);
	va_end(args);
	fputs("\n", stderr);

	size_t instruction = vm.ip - vm.chunk->code - 1;
	int line = vm.chunk->lines[instruction];
	fprintf(stderr, "[line %d] in script\n", line);
	reset_stack();
}

static Value
peek(int distance)
{
	return vm.stack_top[-1 - distance];
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
		case OP_NEGATE:
			if (IS_NUMBER(peek(0))) {
				runtime_error("Operand must be a number.");
				return INTERPRET_RUNTIME_ERROR;
			}
			push(AS_NUMBER(-NUMBER_VAL(pop())));
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

Interpret_res interpret(const char* src)
{
	Chunk chunk;
	init_chunk(&chunk);
	if (!compile(src, &chunk)) {
		free_chunk(&chunk);
		return INTERPRET_COMPILE_ERROR;
	}

	vm.chunk = &chunk;
	vm.ip = vm.chunk->code;

	Interpret_res res = run();

	free_chunk(&chunk);
	return res;
}
