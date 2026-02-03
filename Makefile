example: example.c
	gcc example.c -o example -fno-stack-protector -no-pie -mgeneral-regs-only -g

clean:
	rm example
