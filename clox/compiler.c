#include <stdio.h>

#include "common.h"
#include "compiler.h"
#include "scanner.h"

void
compile(const char *src)
{
	int line = -1;
	init_scanner(src);
	for (;;) {
		Token token = scan_token();
		if (token.line != line) {
			printf("%4d ", token.line);
			line = token.line;
		} else {
			printf("   | ");
		}
		printf("%2d '%.*s'\n", token.type, token.len, token.start);
		if (token.type == TOKEN_EOF) break;
	}
}