#include "common.h"
#include "chunk.h"
#include "debug.h"
#include "vm.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void
repl(void)
{
	char line[1024];
	for (;;) {
		printf("> ");

		if (!fgets(line, sizeof(line), stdin)) {
			printf("\n");
			break;
		}
		interpret(line);
	}
}

static char *
read_file(const char *path)
{
	FILE *file = fopen(path, "rb");
	if (file == NULL) {
		fprintf(stderr, "Could not open file \"%s\".\n", path);
		exit(74);
	}
	fseek(file, 0L, SEEK_END);
	size_t size = ftell(file);
	rewind(file);

	char *buffer = (char *) malloc(size + 1);
	if (buffer == NULL) {
		fprintf(stderr, "Not enough memory to read \"%s\".\n", path);
		exit(74);
	}
	size_t bytes_read = fread(buffer, sizeof(char), size, file);
	if (bytes_read < size) {
		fprintf(stderr, "Could not read file \"%s\".\n", path);
		exit(74);
	}
	buffer[bytes_read] = '\0';
	fclose(file);
	return buffer;
}

static void
run_file(const char *path)
{
	char *src = read_file(path);
	Interpret_res res = interpret(src);
	free(src);

	if (res == INTERPRET_COMPILE_ERROR) exit(65);
	if (res == INTERPRET_RUNTIME_ERROR) exit(70);
}

int
main(int argc, const char* argv[])
{
	initVM();

	if (argc == 1) {
		repl();
	} else if (argc == 2) {
		run_file(argv[1]);
	} else {
		fprintf(stderr, "Usage: clox [path]\n");
	}

	freeVM();
	return 0;
}