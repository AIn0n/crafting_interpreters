#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "compiler.h"
#include "scanner.h"

typedef struct {
	Token current;
	Token previous;
	bool had_error;
	bool panic_mode;
} Parser;

Parser parser;


static void
error_at(Token *token, const char *msg)
{
	if (parser.panic_mode)
		return;

	parser.panic_mode = true;
	fprintf(stderr, "[line %d] Error", token->line);

	if (token->type == TOKEN_EOF) {
		fprintf(stderr, "at end");
	} else if (token->type == TOKEN_ERROR) {
		// nothing
	} else {
		fprintf(stderr, " at '%.*s'", token->len, token->start);
	}

	fprintf(stderr, ": %s\n", msg);
	parser.had_error = true;
}

static void
error(const char *msg)
{
	error_at(&parser.previous, msg);
}

static void
error_at_current(const char *msg)
{
	error_at(&parser.current, msg);
}



static void
advance()
{
	parser.previous = parser.current;

	for (;;) {
		parser.current = scan_token();
		if (parser.current.type != TOKEN_ERROR)
			break;
		error_at_current(parser.current.start);
	}
}

static void
consume(TokenType type, const char *msg)
{
	if (parser.current.type == type)
		return advance();
	
	error_at_current(msg);
}


bool
compile(const char *src, Chunk *chunk)
{
	init_scanner(src);

	parser.had_error = false;
	parser.panic_mode = false;

	advance();
	expression();
	consume(TOKEN_EOF, "Expected EOF");
	return !parser.had_error;
}