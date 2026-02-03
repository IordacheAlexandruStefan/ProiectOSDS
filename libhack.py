from elftools.elf.elffile import ELFFile

class libhack:

	def __init__(self, path):
		self.offset = 0
		self.symbols = { }
		self.data = None

		with open(path, "rb") as f:
			elf = ELFFile(f)
			section = elf.get_section_by_name(".dynsym")
			for symbol in section.iter_symbols():
				self.symbols[symbol.name] = symbol['st_value']

		with open(path, "rb") as f:
			self.data = f.read()

	def getSymbol(self, symbol_name):
		return self.offset + self.symbols[symbol_name]

	def setOffset(self, address, symbol_name):
		self.offset = address - self.getSymbol(symbol_name)

	def search(self, byte_sequence):
		address = self.data.find(byte_sequence)
		if address == -1:
			return 0
		return self.offset + address
