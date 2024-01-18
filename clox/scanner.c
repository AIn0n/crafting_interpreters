#include <stdio.h>
#include <string.h>

#include "common.h"
#include "scanner.h"

typedef struct {
	const char *start;
	const char *curr;
	int line;
} Scanner;

Scanner scanner;

void
init_scanner(const char *src)
{
	scanner.start = src;
	scanner.curr = src;
	scanner.line = 1;
}