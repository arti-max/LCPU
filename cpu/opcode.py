class Opcode:
    def __init__(self, cpu):
        self._cpu = cpu
        self._list = {
            0x00: self.nop,
            0x01: self.lda,
            0x02: self.ldb,
            0x03: self.ldc,
            0x04: self.ldd,
            0x05: self.add_a,
            0x06: self.add_b,
            0x07: self.add_c,
            0x08: self.add_d,
            0x09: self.shl,
            0x0A: self.shr,
            0x0B: self.xor_a,
            0x0C: self.xor_b,
            0x0D: self.xor_c,
            0x0E: self.xor_d,
            0x0F: self.jmp,
            0x10: self.swb,
            0x11: self.cmp_a,
            0x12: self.cmp_b,
            0x13: self.cmp_c,
            0x14: self.cmp_d,
            0x15: self.sub_a,
            0x16: self.sub_b,
            0x17: self.sub_c,
            0x18: self.sub_d,
            0x19: self.and_a,
            0x1A: self.and_b,
            0x1B: self.and_c,
            0x1C: self.and_d,
            0x1D: self.or_a,
            0x1E: self.or_b,
            0x1F: self.or_c,
            0x20: self.or_d,
            0x21: self.je,
            0x22: self.jne,
            0x23: self.jg,
            0x24: self.jl,
            0xFF: self.hlt,
            0x30: self.in_port0,
            0x31: self.in_port1,
            0x32: self.in_port2,
            0x33: self.in_port3,
            0x34: self.out_port0,
            0x35: self.out_port1,
            0x36: self.out_port2,
            0x37: self.out_port3,
            0x40: self.ld_m,
            0x41: self.str_m,
            0x50: self.call,
            0x51: self.ret,
            0x52: self.push,
            0x53: self.pop,
            0x54: self.pushr,
            0x55: self.popr,
            0x60: self.mov_a,
            0x61: self.mov_b,
            0x62: self.mov_c,
            0x63: self.mov_d,
            0x64: self.mov_ir,
            0x65: self.mov_br,
            0x66: self.mov_sp,
            0x67: self.mov_bp,
            0x70: self.ld_ra,
            0x71: self.ld_rb,
            0x72: self.ld_rc,
            0x73: self.ld_rd,
            0x74: self.str_ra,
            0x75: self.str_rb,
            0x76: self.str_rc,
            0x77: self.str_rd,
        }
        
    def nop(self):  # No Operation [0x00]
        pass
         
    def lda(self):  # Load A [0x01]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        val = self._cpu._regs[0x04].value
        self._cpu._regs[0x00].value = val
        
    def ldb(self):  # Load B [0x02]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        val = self._cpu._regs[0x04].value
        self._cpu._regs[0x01].value = val
        
    def ldc(self):  # Load C [0x03]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        val = self._cpu._regs[0x04].value
        self._cpu._regs[0x02].value = val
        
    def ldd(self):  # Load D [0x04]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        val = self._cpu._regs[0x04].value
        self._cpu._regs[0x03].value = val
        
    def add_a(self): # ADD A R [0x05]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x00].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.add(ra, reg)
        self._cpu._regs[0x00].value = res
    
    def add_b(self): # ADD B R [0x06]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x01].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.add(ra, reg)
        self._cpu._regs[0x01].value = res
        
    def add_c(self): # ADD C R [0x07]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x02].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.add(ra, reg)
        self._cpu._regs[0x02].value = res
        
    def add_d(self): # ADD D R [0x08]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x03].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.add(ra, reg)
        self._cpu._regs[0x03].value = res
        
    def shl(self): # SHL R [0x09]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.shift_left(reg)
        reg = self._cpu._regs[reg].value = res
        
    def shr(self): # SHR R [0x0A]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.shift_right(reg)
        reg = self._cpu._regs[reg].value = res
        
    def xor_a(self): # XOR A R [0x0B]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x00].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.xor(reg, ra)
        reg = self._cpu._regs[0x00].value = res
        
    def xor_b(self): # XOR B R [0x0C]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x01].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.xor(reg, ra)
        reg = self._cpu._regs[0x01].value = res
        
    def xor_c(self): # XOR C R [0x0D]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x02].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.xor(reg, ra)
        reg = self._cpu._regs[0x02].value = res
        
    def xor_d(self): # XOR D R [0x0E]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x03].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.xor(reg, ra)
        reg = self._cpu._regs[0x03].value = res
        
    def jmp(self): # JMP ADDR [0x0F]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value
        self._cpu._cu.jmp_bank_check()
        self._cpu._ip.value = addr
        
    def swb(self): # SWB B [0x10]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        bank = self._cpu._regs[0x04].value
        self._cpu._regs[0x05].value = bank
        
    def cmp_a(self): # CMP A R [0x11]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        ra = self._cpu._regs[0x00].value
        self._cpu._alu.sub(ra, reg)
        
    def cmp_b(self): # CMP B R [0x12]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        ra = self._cpu._regs[0x01].value
        self._cpu._alu.sub(ra, reg)
        
    def cmp_c(self): # CMP C R [0x13]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        ra = self._cpu._regs[0x02].value
        self._cpu._alu.sub(ra, reg)
        
    def cmp_d(self): # CMP D R [0x14]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        reg = self._cpu._regs[reg].value
        ra = self._cpu._regs[0x03].value
        self._cpu._alu.sub(ra, reg)
        
    def sub_a(self): # SUB A R [0x15]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x00].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.sub(ra, reg)
        self._cpu._regs[0x00].value = res
    
    def sub_b(self): # SUB B R [0x16]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x01].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.sub(ra, reg)
        self._cpu._regs[0x01].value = res
        
    def sub_c(self): # SUB C R [0x17]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x02].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.sub(ra, reg)
        self._cpu._regs[0x02].value = res
        
    def sub_d(self): # SUB D R [0x18]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x03].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.sub(ra, reg)
        self._cpu._regs[0x03].value = res
        
    def and_a(self): # AND A R [0x19]
        # [opcode] [operand] {2-bytes}
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x00].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.and_(ra, reg)
        self._cpu._regs[0x00].value = res
        
    def and_b(self): # AND B R [0x1A]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x01].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.and_(ra, reg)
        self._cpu._regs[0x01].value = res
        
    def and_c(self): # AND C R [0x1B]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x02].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.and_(ra, reg)
        self._cpu._regs[0x02].value = res
        
    def and_d(self): # AND D R [0x1C]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x03].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.and_(ra, reg)
        self._cpu._regs[0x03].value = res
        
    def or_a(self): # OR A R [0x1D]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x00].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.or_(ra, reg)
        self._cpu._regs[0x00].value = res
        
    def or_b(self): # OR B R [0x1E]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x01].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.or_(ra, reg)
        self._cpu._regs[0x01].value = res
        
    def or_c(self): # OR C R [0x1F]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x02].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.or_(ra, reg)
        self._cpu._regs[0x02].value = res
        
    def or_d(self): # OR D R [0x20]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        ra = self._cpu._regs[0x03].value
        reg = self._cpu._regs[reg].value
        res = self._cpu._alu.or_(ra, reg)
        self._cpu._regs[0x03].value = res
        
    def je(self): # JE addr [0x21]
        # Jump if Zero flag is set
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value
        if self._cpu._flags[0x00].value:
            self._cpu._cu.jmp_bank_check()
            self._cpu._ip.value = addr
            
    def jne(self): # JNE addr [0x22]
        # Jump if Zero flag is not set
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value
        if not self._cpu._flags[0x00].value:
            self._cpu._cu.jmp_bank_check()
            self._cpu._ip.value = addr
            
    def jg(self): # JG addr [0x23]
        # Jump if Sign flag equals Overflow flag and Zero flag is clear
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value
        if (self._cpu._flags[0x02].value == self._cpu._flags[0x03].value) and not self._cpu._flags[0x00].value:
            self._cpu._cu.jmp_bank_check()
            self._cpu._ip.value = addr
            
    def jl(self): # JL addr [0x24]
        # Jump if Sign flag not equals Overflow flag
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value
        if self._cpu._flags[0x02].value != self._cpu._flags[0x03].value:
            self._cpu._cu.jmp_bank_check()
            self._cpu._ip.value = addr
        
    def hlt(self): # HLT [0xFF]
        # [opcode] {1-byte}
        self._cpu.running = False
        
    def in_port0(self): # IN 0,R [0x30]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value  # Получаем номер регистра из операнда
        device = self._cpu._device_manager.get_device(0)
        if device:
            self._cpu._regs[reg].value = device.IN()
            
    def in_port1(self): # IN 1,R [0x31]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(1)
        if device:
            self._cpu._regs[reg].value = device.IN()
            
    def in_port2(self): # IN 2,R [0x32]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(2)
        if device:
            self._cpu._regs[reg].value = device.IN()
            
    def in_port3(self): # IN 3,R [0x33]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(3)
        if device:
            self._cpu._regs[reg].value = device.IN()
    
    def out_port0(self): # OUT 0,R [0x34]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(0)
        if device:
            device.OUT(self._cpu._regs[reg].value)
            
    def out_port1(self): # OUT 1,R [0x35]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(1)
        if device:
            device.OUT(self._cpu._regs[reg].value)
            
    def out_port2(self): # OUT 2,R [0x36]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(2)
        if device:
            device.OUT(self._cpu._regs[reg].value)
            
    def out_port3(self): # OUT 3,R [0x37]
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        device = self._cpu._device_manager.get_device(3)
        if device:
            device.OUT(self._cpu._regs[reg].value)
        
    def _memory_operation(self, operation, bank=None):
        """Выполнить операцию с памятью с сохранением текущего банка"""
        addr = self._cpu._regs[0x04].value
        
        # Если указан банк, переключаемся на него
        if bank is not None:
            # Сохраняем текущий банк
            current_bank = self._cpu._memory.current_bank
            # Переключаемся на нужный банк
            self._cpu._memory.current_bank = bank
            
            # Выполняем операцию
            result = operation(addr)
            
            # Возвращаем исходный банк
            self._cpu._memory.current_bank = current_bank
            return result
        else:
            # Если банк не указан, просто выполняем операцию в текущем банке
            return operation(addr)

    def ld_m(self): # LD M [0x40] addr
        """Загрузить значение из памяти в аккумулятор"""
        self._cpu._cu.fetch()  # Получаем адрес
        bank = self._cpu._regs[0x05].value
        
        def operation(addr):
            return self._cpu._memory.get_byte(addr)
        
        value = self._memory_operation(operation, bank)
        self._cpu._regs[0x00].value = value  # Загружаем в A

    def str_m(self): # STR M [0x41] addr
        """Сохранить значение из аккумулятора в память"""
        self._cpu._cu.fetch()  # Получаем адрес
        bank = self._cpu._regs[0x05].value
        
        def operation(addr):
            self._cpu._memory.get_byte(addr, self._cpu._regs[0x00].value)
            return None
        
        self._memory_operation(operation, bank)
        
    def call(self): # CALL [0x50] addr
        """Вызов подпрограммы"""
        # Получаем адрес перехода
        self._cpu._cu.fetch()
        addr = self._cpu._regs[0x04].value  # IR
        
        # Сохраняем текущий банк
        current_bank = self._cpu._regs[0x05].value  # BR
        
        # Переключаемся на банк стека (банк 3)
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Сохраняем адрес возврата (PC) в стек
        self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, self._cpu._ip.value)  # SP -> адрес возврата
        self._cpu._regs[0x06].value -= 1  # Уменьшаем SP
        
        # Сохраняем номер банка в стек
        self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, current_bank)  # SP -> номер банка
        self._cpu._regs[0x06].value -= 1  # Уменьшаем SP
        
        # Переключаемся на нужный банк и переходим по адресу
        self._cpu._regs[0x05].value = current_bank  # Восстанавливаем BR
        self._cpu._cu.jmp_bank_check()  # Проверяем и переключаем банк если нужно
        self._cpu._ip.value = addr

    def ret(self):  # RET [0x51]
        """Возврат из подпрограммы с очисткой стека"""
        # Сохраняем текущий банк
        self._cpu._cu.fetch()
        current_bank = self._cpu._regs[0x05].value  # BR
        clr_data = self._cpu._regs[0x04].value-1
        
        # Переключаемся на банк стека (банк 0)
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Увеличиваем SP
        self._cpu._regs[0x06].value += 1
        
        # Получаем номер банка из стека
        return_bank = self._cpu._memory.get_byte(self._cpu._regs[0x06].value)
        
        # Увеличиваем SP
        self._cpu._regs[0x06].value += 1
        
        # Получаем адрес возврата из стека
        return_addr = self._cpu._memory.get_byte(self._cpu._regs[0x06].value)
        
        #print(f"RET: Bank: {return_bank} | Addr: {return_addr} | CBk: {self._cpu._regs[0x05].value} & CbkM: {self._cpu._memory._current_bank}")
        
        # Очищаем память в стеке
        for i in range(1+clr_data):  # Очищаем два байта (номер банка и адрес возврата) + пользовательские данные
            self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, 0x00)
            self._cpu._regs[0x06].value += 1
        
        # Переключаемся на банк возврата
        self._cpu._regs[0x05].value = return_bank
        self._cpu._cu.jmp_bank_check()  # Проверяем и переключаем банк если нужно
        self._cpu._ip.value = return_addr

    def push(self): # PUSH [0x52] reg
        """Сохранить значение регистра в стек"""
        # Получаем номер регистра
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        
        # Переключаемся на банк стека
        current_bank = self._cpu._regs[0x05].value
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Сохраняем значение в стек
        self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, self._cpu._regs[reg].value)
        self._cpu._regs[0x06].value -= 1
        
        # Возвращаемся в исходный банк
        self._cpu._regs[0x05].value = current_bank
        self._cpu._memory._current_bank = current_bank

    def pop(self): # POP [0x53] reg
        """Восстановить значение из стека в регистр"""
        # Получаем номер регистра
        self._cpu._cu.fetch()
        reg = self._cpu._regs[0x04].value
        
        # Переключаемся на банк стека
        current_bank = self._cpu._regs[0x05].value
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Увеличиваем SP и читаем значение
        self._cpu._regs[0x06].value += 1
        value = self._cpu._memory.get_byte(self._cpu._regs[0x06].value)
        self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, 0x00)
        
        # Восстанавливаем значение в регистр
        self._cpu._regs[reg].value = value
        
        # Возвращаемся в исходный банк
        self._cpu._regs[0x05].value = current_bank
        self._cpu._memory._current_bank = current_bank

    def pushr(self): # PUSHR [0x54]
        """Сохранить все регистры в стек"""
        # Переключаемся на банк стека
        current_bank = self._cpu._regs[0x05].value
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Сохраняем регистры в обратном порядке (кроме SP)
        for reg in range(5, -1, -1):  # от 5 до 0
            self._cpu._memory.wr_byte(self._cpu._regs[0x06].value, self._cpu._regs[reg].value)
            self._cpu._regs[0x06].value -= 1
        
        # Возвращаемся в исходный банк
        self._cpu._regs[0x05].value = current_bank
        self._cpu._memory._current_bank = current_bank

    def popr(self): # POPR [0x55]
        """Восстановить все регистры из стека"""
        # Переключаемся на банк стека
        current_bank = self._cpu._regs[0x05].value
        self._cpu._regs[0x05].value = 0x00
        self._cpu._memory._current_bank = 0x00
        
        # Восстанавливаем регистры в прямом порядке (кроме SP)
        for reg in range(0, 6):  # от 0 до 5
            self._cpu._regs[0x06].value += 1
            value = self._cpu._memory.get_byte(self._cpu._regs[0x06].value)
            self._cpu._regs[reg].value = value
        
        # Возвращаемся в исходный банк
        self._cpu._regs[0x05].value = current_bank
        self._cpu._memory._current_bank = current_bank

    def mov_a(self):  # MOV A, reg [0x60]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x00].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_b(self):  # MOV B, reg [0x61]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x01].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_c(self):  # MOV C, reg [0x62]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x02].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_d(self):  # MOV D, reg [0x63]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x03].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_ir(self):  # MOV IR, reg [0x64]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x04].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_br(self):  # MOV BR, reg [0x65]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x05].value = (self._cpu._regs[src_reg].value + offset) & 0xF  # BR только 4 бита

    def mov_sp(self):  # MOV SP, reg [0x66]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x06].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def mov_bp(self):  # MOV BP, reg [0x67]
        self._cpu._cu.fetch()  # получаем регистр-источник
        src_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        self._cpu._regs[0x07].value = (self._cpu._regs[src_reg].value + offset) & 0xFF

    def ld_ra(self):  # LD RA, [reg+offset] [0x70]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        cur_bank = self._cpu._memory._current_bank
        self._cpu._memory._current_bank = self._cpu._regs[0x05].value # BR

        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        #print(f"LD-RA: {self._cpu._memory.get_byte(addr)}")
        self._cpu._regs[0x00].value = self._cpu._memory.get_byte(addr)
        self._cpu._memory._current_bank = cur_bank
        self._cpu._regs[0x05].value = cur_bank

    def ld_rb(self):  # LD RB, [reg+offset] [0x71]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._regs[0x01].value = self._cpu._memory.get_byte(addr)

    def ld_rc(self):  # LD RC, [reg+offset] [0x72]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._regs[0x02].value = self._cpu._memory.get_byte(addr)

    def ld_rd(self):  # LD RD, [reg+offset] [0x73]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._regs[0x03].value = self._cpu._memory.get_byte(addr)

    def str_ra(self):  # STR [reg+offset], A [0x74]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._memory.get_byte(addr, self._cpu._regs[0x00].value)

    def str_rb(self):  # STR [reg+offset], B [0x75]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._memory.get_byte(addr, self._cpu._regs[0x01].value)

    def str_rc(self):  # STR [reg+offset], C [0x76]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._memory.get_byte(addr, self._cpu._regs[0x02].value)

    def str_rd(self):  # STR [reg+offset], D [0x77]
        self._cpu._cu.fetch()  # получаем регистр-адрес
        addr_reg = self._cpu._regs[0x04].value
        self._cpu._cu.fetch()  # получаем смещение
        offset = self._cpu._regs[0x04].value
        
        addr = (self._cpu._regs[addr_reg].value + offset) & 0xFF
        self._cpu._memory.get_byte(addr, self._cpu._regs[0x03].value)
        
        
        
        
        
        
    
        