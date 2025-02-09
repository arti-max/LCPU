
class Register16:
    """16-bit register class [0x0000 - 0xFFFF]"""
    def __init__(self):
        self._value = 0x0000
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, data):
        self._value = data & 0xFFFF
        
    def __repr__(self):
        return f"0x{self._value:04X}"

class Register8:
    """8-bit register class [0x00 - 0xFF]"""
    def __init__(self):
        self._value = 0x00
        
    @property
    def value(self):
        return self._value & 0xFF
    
    @value.setter
    def value(self, data):
        self._value = data & 0xFF
        
    def __repr__(self):
        return f"0x{self._value:02X}"
    
class Register4:
    """4-bit register class [0x0 - 0xF]"""
    def __init__(self):
        self._value = 0x0
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, data):
        self._value = data & 0xF
        
    def __repr__(self):
        return f"0x{self._value:01X}"
        
class RegisterBit:
    """1-bit register class [0x0 - 0x1]"""
    def __init__(self):
        self._value = 0x0
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, data):
        self._value = data & 0x3
        
    def __repr__(self):
        return f"0x{self._value:01X}"