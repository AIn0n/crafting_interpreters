#ifndef _DEBUG_H_
#define _DEBUG_H_

#include "chunk.h"

void disassemble_chunk(Chunk *chunk, const char *name);
int disassemble_instr(Chunk *Chunk, int offset);

#endif