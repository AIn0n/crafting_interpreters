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
allocateString(char *chars, int len)
{
	ObjString* string = ALLOCATE_OBJ(ObjString, OBJ_STRING);
	string->len = len;
	string->chars = chars;
	return string;
}

ObjString*
copyString(char *chars, int len)
{
	char* heap_chars = ALLOCATE(char, len + 1);
	memcpy(heap_chars, chars, len);
	heap_chars[len] = '\0';
	return allocateString(heap_chars, len);
}

ObjString*
takeString(char *chars, int len)
{
	return allocateString(chars, len);
}
