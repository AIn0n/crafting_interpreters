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

static char
peek_next()
{
	if (is_at_end())
		return '\0';
	return scanner.curr[1];
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
		case '/':
			if (peek_next() == '/') {
				while (peek() != '\n' && !is_at_end())
					advance();
			} else
				return;
			break;
		default:
			return;
		}
	}
}

static Token
string()
{
	while (peek() != '"' && !is_at_end()) {
		if (peek() == '\n')
			scanner.line++;
		advance();
	}
	if (is_at_end())
		return error_token("Unterterminated string.");
	
	advance(); // consume closing bracket
	return make_token(TOKEN_STRING);
}

static bool
is_digit(const char c)
{
	return c >= '0' && c <= '9';
}

static Token
number()
{
	while (is_digit(peek()))
		advance();
	
	if (peek() == '.' && is_digit(peek_next())) {
		advance();

		while (is_digit(peek()))
			advance();
	}

	return make_token(TOKEN_NUMBER);
}

static bool
is_alpha(const char c)
{
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

static TokenType
identifier_type()
{
	return TOKEN_IDENTIFIER;
}

static Token
identifier()
{
	while (is_alpha(peek()) || is_digit(peek()))
		advance();
	return make_token(identifier_type());
}

Token
scan_token(void)
{
	skip_whitespaces();
	scanner.start = scanner.curr;

	if (is_at_end()) return make_token(TOKEN_EOF);

	char c = advance();

	if (is_alpha(c))
		return identifier();

	if (is_digit(c))
		return number();

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
	case '"':
		return string();
	}

	return error_token("unexpected character");
}