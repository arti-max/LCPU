from cpu.register import Register8, Register4, Register16, RegisterBit   # register classes
from cpu.opcode import Opcode
from cpu.alu import Alu
from cpu.control_unit import ControlUnit



class CPU:
    def __init__(self, ram, device_manager=None):
        self._regs = {
            # POH
            0x00: Register8(),  # A [8-bit]
            0x01: Register8(),  # B [8-bit]
            0x02: Register8(),  # C [8-bit]
            0x03: Register4(),  # D [4-bit]
            # NPOH
            0x04: Register8(),  # IR [8-bit] - Instruction Register
            0x05: Register4(),  # BR [4-bit] - Bank Register
            0x06: Register8(),  # SP [8-bit] - Stack Pointer
            0x07: Register8(),  # BP [8-bit] - Base Pointer
        }
        self._flags = {
            0x00: RegisterBit(), # Zero
            0x01: RegisterBit(), # Carry
            0x02: RegisterBit(), # Sign
            0x03: RegisterBit(), # Overflow
        }
        
        self._ip = Register16() # Instruction Pointer [16-bit]
        
        self._alu = Alu(self)   
        self._opcode = Opcode(self)
        self._cu = ControlUnit(self)
        self._memory = ram
        
        self.running = False
        self._device_manager = device_manager
        
    def initialize(self, load_func):
        """Инициализация процессора"""
        # Регистры:
        # 0x00 - A (аккумулятор)
        # 0x01 - B
        # 0x02 - C
        # 0x03 - D
        # 0x04 - BR (Bank Register)
        # 0x05 - SP (Stack Pointer)
        self._regs = {
            0x00: Register8(),  # A
            0x01: Register8(),  # B
            0x02: Register8(),  # C
            0x03: Register4(),  # D
            0x04: Register8(),  # IR
            0x05: Register4(),  # BP
            0x06: Register8(),  # SP
            0x07: Register8(),  # BP
        }
        
        # Сброс всех регистров
        for reg in self._regs.values():
            reg.value = 0
            
        # Сброс всех флагов
        for flag in self._flags.values():
            flag.value = 0
            
        # Сброс указателя инструкций
        self._ip.value = 0

        # Инициализируем SP, BP значением 0x9F
        self._regs[0x06].value = 0x9F
        self._regs[0x07].value = 0x9F

        # Очистка памяти
        self._memory.clear()
        
        # Вызов функции загрузки
        load_func(self)  # Передаем CPU в load_func
        
    def set_flag(self, name, value):
        #print(f"set flag: {name} | {int(value)}")
        self._flags[name].value = int(value)
    
    def step(self):
        """Выполнить один шаг процессора"""
        if self.running:
            self._cu.fetch()    # Fetch Instruction
            print(f"Regs: {self._regs} | Flags: {self._flags} | Ip: {self._ip}") # | Bank 4: {self._memory._memory[3]._data}  | Bank 1: {self._memory._memory[0]._data}
            opcode = self._opcode._list[self._regs[0x04].value]
            opcode()

    def run(self):
        """Запустить процессор в непрерывном режиме"""
        self.initialize()
        while self.running:
            self.step()