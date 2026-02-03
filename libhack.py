from pwn import ELF

class libhack:

	def __init__(self, path):
		self.elf = ELF(path)
		self.offset = 0
		self.path = path

	def getSymbol(self, symbol_name):
		if symbol_name not in self.elf.symbols:
			raise ValueError(f"Symbol '{symbol_name}' not found in {self.path}")
		return self.offset + self.elf.symbols[symbol_name]

	def setOffset(self, leaked_address, symbol_name):
		if symbol_name not in self.elf.symbols:
			raise ValueError(f"Symbol '{symbol_name}' not found in {self.path}")
		self.offset = leaked_address - self.elf.symbols[symbol_name]

	def search(self, byte_sequence):
		result = next(self.elf.search(byte_sequence), None)
		if result is None:
			raise ValueError(f"Byte sequence {byte_sequence} not found in {self.path}")
		return self.offset + result
