class Bank:
    def __init__(self, size=256):
        self._size = size
        self._data = bytearray(self._size)
        
    def bank_get_byte(self, addr):
        return self._data[addr]
    
    def bank_wr_byte(self, addr, value):
        value = value & 0xFF
        self._data[addr] = value
        
        
        
class Ram:
    def __init__(self, banks=4):
        self._banks = banks
        self._size = Bank()._size
        self._memory = [Bank() for _ in range(self._banks)]
        self._current_bank = 0x00
        
        
    def get_byte(self, addr):
        return self._memory[self._current_bank].bank_get_byte(addr)
    
    def wr_byte(self, addr, data):
        self._memory[self._current_bank].bank_wr_byte(addr, data)
        
    def switch_bank(self, bank=0x00):
        self._current_bank = bank

    def clear(self):
        """Очистка памяти"""
        self._memory = [Bank() for _ in range(self._banks)]