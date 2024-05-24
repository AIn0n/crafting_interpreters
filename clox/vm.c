#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#include "common.h"
#include "debug.h"
#include "vm.h"
#include "compiler.h"
#include "object.h"
#include "memory.h"

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
	vm.objects = NULL;
}

void
freeVM()
{
	free_objects();
}

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

static bool
isFalsey(Value value)
{
	return IS_NIL(value) || (IS_BOOL(value) && !AS_BOOL(value));
}

static void
concatenate()
{
	ObjString *a = AS_STRING(pop());
	ObjString *b = AS_STRING(pop());

	int len = a->len + b->len;
	char *chars = ALLOCATE(char, len + 1);
	memcpy(chars, a->chars, a->len);
	memcpy(chars + a->len, b->chars, b->len);
	chars[len] = '\0';
	
	ObjString *res = takeString(chars, len);
	push(OBJ_VAL(res));
}

static Interpret_res
run()
{
#define READ_BYTE() (*vm.ip++)
#define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])
#define BINARY_OP(val_type, op)						\
	do {								\
		if (!IS_NUMBER(peek(0)) || !IS_NUMBER(peek(1))) {	\
			runtime_error("Operands must be numbers.");	\
			return INTERPRET_RUNTIME_ERROR;			\
		}							\
		double b = AS_NUMBER(pop());				\
		double a = AS_NUMBER(pop());				\
		push(val_type(a op b));					\
	} while (false)

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
			push(NUMBER_VAL(-AS_NUMBER(pop())));
			break;
		case OP_NIL:
			push(NIL_VAL);
			break;
		case OP_TRUE:
			push(BOOL_VAL(true));
			break;
		case OP_FALSE:
			push(BOOL_VAL(false));
			break;
		case OP_EQUAL: {
			Value b = pop();
			Value a = pop();
			push(BOOL_VAL(valuesEqual(a, b)));
			break;
		}
		case OP_GREATER:	BINARY_OP(BOOL_VAL,	>);	break;
		case OP_LESS:		BINARY_OP(BOOL_VAL,	<);	break;
		case OP_ADD:
			if (IS_STRING(peek(0)) && IS_STRING(peek(1))) {
				concatenate();
			} else if (IS_NUMBER(peek(0)) && IS_NUMBER(peek(1))) {
				double a = AS_NUMBER(pop());
				double b = AS_NUMBER(pop());
				push(NUMBER_VAL(a + b));
			} else {
				runtime_error("both operands must be the same type.");
				return INTERPRET_RUNTIME_ERROR;
			}
			break;
		case OP_SUB:		BINARY_OP(NUMBER_VAL,	-);	break;
		case OP_MUL:		BINARY_OP(NUMBER_VAL,	*);	break;
		case OP_DIV:		BINARY_OP(NUMBER_VAL,	/);	break;

		case OP_NOT:
			push(BOOL_VAL(isFalsey(pop())));
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
