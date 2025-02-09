
class ControlUnit:
    def __init__(self, cpu):
        self._cpu = cpu
        
    def fetch(self):
        self._cpu._regs[0x04].value = self._cpu._memory.get_byte(self._cpu._ip.value)
        self._cpu._ip.value += 1
        
    def jmp_bank_check(self):
        self._cpu._memory._current_bank = self._cpu._regs[0x05].value