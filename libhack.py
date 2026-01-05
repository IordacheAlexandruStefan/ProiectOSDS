class libhack:

    def __init__(self):
        self.offset = 0

    def getSymbol(self, symbol_name):
        return self.offset # + 0x1000
    
    def setOffset(self, address, symbol_name):
        self.offset = address - self.getSymbol(symbol_name)

    def search(self, byte_sequence):
        return self.offset # + 0x2000