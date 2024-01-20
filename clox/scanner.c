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

static bool 
is_at_end(void)
{
	return *scanner.curr == '\0';
}

static Token
make_token(TokenType type)
{
	return (Token) {
		.type = type,
		.start = scanner.start,
		.len = (int) (scanner.curr - scanner.start),
		.line = scanner.line
	};
}

static Token
error_token(const char *msg)
{
	return (Token) {
		.type = TOKEN_ERROR,
		.start = msg,
		.len = (int) strlen(msg),
		.line = scanner.line
	};
}

Token
scan_token(void)
{
	scanner.start = scanner.curr;

	if (is_at_end()) return make_token(TOKEN_EOF);

	return error_token("unexpected character");
}