#include <stdio.h>

#include "common.h"
#include "compiler.h"
#include "scanner.h"

bool
compile(const char *src, Chunk *chunk)
{
	init_scanner(src);
	advance();
	expression();
	consume(TOKEN_EOF, "Expected EOF");
	return false;
}