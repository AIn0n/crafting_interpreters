#ifndef _CLOX_COMPILER_H_
#define _CLOX_COMPILER_H_

#include "vm.h"

bool compile(const char *src, Chunk* chunk);

#endif