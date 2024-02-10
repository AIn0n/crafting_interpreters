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
}
Parser;

typedef enum {
	PREC_NONE,
	PREC_ASSIGNMENT,  // =
	PREC_OR,          // or
	PREC_AND,         // and
	PREC_EQUALITY,    // == !=
	PREC_COMPARISON,  // < > <= >=
	PREC_TERM,        // + -
	PREC_FACTOR,      // * /
	PREC_UNARY,       // ! -
	PREC_CALL,        // . ()
	PREC_PRIMARY
}
Precedence;


Parser parser;
Chunk *compiling_chunk;

static Chunk*
current_chunk()
{
	return compiling_chunk;
}


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

static void
emit_byte(uint8_t byte)
{
	write_chunk(current_chunk(), byte, parser.previous.line);

}

static void
emit_bytes(uint8_t byte1, uint8_t byte2)
{
	emit_byte(byte1);
	emit_byte(byte2);
}

static void
emit_return()
{
	emit_byte(OP_RETURN);
}

static void
end_compiler()
{
	emit_return();
}

static void
binary()
{
	TokenType operator_type = parser.previous.type;
	ParseRule *rule = get_rule(operator_type);
	parse_precedence((Precedence)(rule->precedence + 1));
	switch (operator_type)
	{
	case TOKEN_PLUS:
		emit_byte(OP_ADD);
		break;
	case TOKEN_MINUS:
		emit_byte(OP_SUB);
		break;
	case TOKEN_STAR:
		emit_byte(OP_MUL);
		break;
	case TOKEN_SLASH:
		emit_byte(OP_DIV);
		break;
	default:
		return;
	}
}

static void expression()
{
	parse_precedence(PREC_ASSIGNMENT);
}

static uint8_t
make_constant(Value val)
{
	int constant = add_constant(current_chunk(), val);
	if (constant > UINT8_MAX) {
		error("Too many constants in one chunk");
		return 0;
	}

	return (uint8_t) constant;
}

static void
emit_constant(Value value)
{
	emit_bytes(OP_CONSTANT, make_constant(value));
}

static void
number()
{
	double val = strtod(parser.previous.start, NULL);
	emit_constant(val);
}

static void
unary()
{
	TokenType operator_type = parser.previous.type;
	

	parse_precedence(PREC_UNARY);

	switch (operator_type)
	{
	case TOKEN_MINUS:
		emit_byte(OP_NEGATE);
		break;
	default:
		return;
	}
}

static void
grouping()
{
	expression();
	consume(TOKEN_RIGHT_PAREN, "Expected ( after expression.");
}

static void
parse_precedence(Precedence precedence)
{

}


bool
compile(const char *src, Chunk *chunk)
{
	init_scanner(src);
	compiling_chunk = chunk;

	parser.had_error = false;
	parser.panic_mode = false;

	advance();
	expression();
	consume(TOKEN_EOF, "Expected EOF");
	end_compiler();
	return !parser.had_error;
}