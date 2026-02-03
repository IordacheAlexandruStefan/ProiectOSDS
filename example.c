#include <stdio.h>

void __attribute__((no_caller_saved_registers)) func(int* x)
{
	*x += 1;
}

int main()
{
	puts("Hello World!");
	char name[32];
	gets(name);
	return 0;
}
