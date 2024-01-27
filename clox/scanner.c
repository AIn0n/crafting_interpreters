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

static char
advance()
{
	scanner.curr++;
	return scanner.curr[-1];
}

static bool match(const char expected) {
	if (is_at_end())
		return false;
	if (*scanner.curr != expected)
		return false;
	scanner.curr++;
	return true;
}

static char 
peek()
{
	return *scanner.curr;
}

static void
skip_whitespaces() 
{
	for (;;) {
		char c = peek();
		switch (c) {
		case ' ':
		case '\r':
		case '\t':
			advance();
			break;
		case '\n':
			advance();
			scanner.line++;
			break;
		default:
			return;
		}
	}
}

Token
scan_token(void)
{
	skip_whitespaces();
	scanner.start = scanner.curr;

	if (is_at_end()) return make_token(TOKEN_EOF);

	char c = advance();
	switch (c) {
	case '(': 
		return make_token(TOKEN_LEFT_PAREN);
	case ')': 
		return make_token(TOKEN_RIGHT_PAREN);
	case '{': 
		return make_token(TOKEN_LEFT_BRACE);
	case '}': 
		return make_token(TOKEN_RIGHT_BRACE);
	case ';': 
		return make_token(TOKEN_SEMICOLON);
	case ',': 
		return make_token(TOKEN_COMMA);
	case '.':
		return make_token(TOKEN_DOT);
	case '-':
		return make_token(TOKEN_MINUS);
	case '+':
		return make_token(TOKEN_PLUS);
	case '/':
		return make_token(TOKEN_SLASH);
	case '*':
		return make_token(TOKEN_STAR);
	case '!':
		return make_token(match('=') ? TOKEN_BANG_EQUAL : TOKEN_BANG);
	case '=':
		return make_token(match('=') ? TOKEN_EQUAL_EQUAL : TOKEN_EQUAL);
	case '<':
		return make_token(match('=') ? TOKEN_LESS_EQUAL : TOKEN_LESS);
	case '>':
		return make_token(match('=') ? TOKEN_GREATER_EQUAL : TOKEN_GREATER);
	}

	return error_token("unexpected character");
}