#include <stdio.h>
#include "stab_alloc.h"

int
main(void)
{
	Stab_data alloc = init_stab();

	printf("-- mem addr = %llu\n", (uint64_t) alloc.mem);
	
	int *a = (int *) salloc(&alloc, sizeof(*a) * 128);

	for (int n = 0; n < 8; ++n) {
		printf("%i ", alloc.len[n]);
	}
	puts("");

	puts("realloc");

	int *b = (int *) salloc(&alloc, sizeof(*b) * 20);

	a = (int *) srealloc(&alloc, a, sizeof(*a) * 200);

	for (int n = 0; n < 8; ++n) {
		printf("%i ", alloc.len[n]);
	}
	puts("");


	sfree(&alloc, a);
	//sfree(&alloc, b);

}
