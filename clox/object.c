#include <stdio.h>
#include <string.h>

#include "memory.h"
#include "object.h"
#include "value.h"
#include "vm.h"

#define ALLOCATE_OBJ(type, objectType) \
	(type*) allocateObject(sizeof(type), objectType)

static Obj*
allocateObject(size_t size, ObjType type)
{
	Obj* object = (Obj *) reallocate(NULL, 0, size);
	object->type = type;

	object->next = vm.objects;
	vm.objects = object;
	return object;
}

static ObjString*
allocateString(char *chars, int len, uint32_t hash)
{
	ObjString* string = ALLOCATE_OBJ(ObjString, OBJ_STRING);
	string->len = len;
	string->chars = chars;
	string->hash = hash;
	return string;
}

static uint32_t hashString(const char* key, int length) {
	uint32_t hash = 2166136261u;
	for (int i = 0; i < length; i++) {
		hash ^= (uint8_t)key[i];
		hash *= 16777619;
	}
	return hash;
}

ObjString*
copyString(char *chars, int len)
{
	uint32_t hash = hashString(chars, len);
	char* heap_chars = ALLOCATE(char, len + 1);
	memcpy(heap_chars, chars, len);
	heap_chars[len] = '\0';
	return allocateString(heap_chars, len, hash);
}

ObjString*
takeString(char *chars, int len)
{
	uint32_t hash = hashString(chars, len);
	return allocateString(chars, len,  hash);
}
