class Alu:
    # zero      - 0x00
    # carry     - 0x01
    # sign      - 0x02
    # overflow  - 0x03
    def __init__(self, cpu):
        self._cpu = cpu  # Исправлено: сохранение ссылки на CPU

    def add(self, a, b):
        """Сложение с установкой флагов."""
        result = (a + b) & 0xFF
        carry = (a + b) > 0xFF
        
        # Установка флагов
        self._cpu.set_flag(0x01, carry)
        self._cpu.set_flag(0x00, result == 0)
        self._cpu.set_flag(0x02, (result >> 7) & 1)  # 7-й бит = знак
        
        # Проверка на переполнение для знаковых чисел
        overflow = ((a ^ result) & (b ^ result)) & 0x80 != 0
        self._cpu.set_flag(0x03, overflow)
        
        return result

    def sub(self, a, b):
        """Вычитание с установкой флагов."""
        result = (a - b) & 0xFF
        borrow = a < b

        #print(f"RSUB: {result} | A: {a}, B: {b}")
        
        # Установка флагов
        self._cpu.set_flag(0x01, borrow)
        self._cpu.set_flag(0x00, result == 0)
        self._cpu.set_flag(0x02, (result >> 7) & 1)
        
        # Проверка на переполнение для знаковых чисел
        overflow = ((a ^ b) & (a ^ result)) & 0x80 != 0
        self._cpu.set_flag(0x03, overflow)
        
        return result

    def and_(self, a, b):
        """Логическое И."""
        result = (a & b) & 0xFF
        self._update_logic_flags(result)
        return result

    def or_(self, a, b):
        """Логическое ИЛИ."""
        result = (a | b) & 0xFF
        self._update_logic_flags(result)
        return result

    def xor(self, a, b):
        """Исключающее ИЛИ."""
        result = (a ^ b) & 0xFF
        self._update_logic_flags(result)
        return result

    def shift_left(self, a):
        """Сдвиг влево с переносом."""
        carry = (a >> 7) & 1
        result = (a << 1) & 0xFF
        self._cpu.set_flag(0x01, carry)
        self._update_logic_flags(result)
        return result
    
    def shift_right(self, a):
        """Сдвиг вправо с переносом."""
        carry = a & 1  # Получаем младший бит (бит, который будет вытолкнут)
        result = (a >> 1) & 0xFF  # Сдвигаем вправо на 1 бит и маскируем, чтобы остаться в пределах 8 бит
        self._cpu.set_flag(0x01, carry) # Устанавливаем флаг переноса в соответствии с вытолкнутым битом
        self._update_logic_flags(result) # Обновляем флаги нуля и отрицательного значения
        return result

    def _update_logic_flags(self, result):
        """Обновление флагов для логических операций."""
        self._cpu.set_flag(0x00, result == 0)
        self._cpu.set_flag(0x02, (result >> 7) & 1)