import sys
from cpu.cpu import CPU
from memory.ram import Ram
from ino.device_manager import DeviceManager
import pygame

def load_programs(cpu):
    """Загрузка программ из файлов b0.bin, b1.bin и т.д. в банки памяти."""
    for bank in range(16):
        try:
            with open(f"boot/b{bank}.bin", "r") as f:
                data = f.read().strip().split()
                for addr, byte in enumerate(data):
                    print(f"addr: {addr} | byte: {byte}")
                    byte = int(byte.strip(), 16)
                    cpu._memory.current_bank = bank
                    cpu._memory.wr_byte(addr, byte)
        except FileNotFoundError:
            pass  # Если файл не найден, пропускаем

def main():
    # Инициализация компонентов
    ram = Ram()
    device_manager = DeviceManager()
    cpu = CPU(ram, device_manager)
    
    # Загрузка устройств и инициализация дисплея
    device_manager.load_devices()
    device_manager.set_cpu(cpu)  # Устанавливаем процессор для устройств
    device_manager.init_display()
    
    # Инициализация процессора
    cpu.initialize(load_programs)
    # Загрузка программ в банки памяти
    device_manager._cpu = cpu
    device_manager._load_prog = load_programs
    
    clock = pygame.time.Clock()
    cpu.running = True
    running = True
    
    while running:
        # Обработка событий pygame
        events = pygame.event.get()
        
        # Передаем события устройствам
        device_manager.handle_events(events)
        
        # Получаем события от устройств
        device_events = device_manager.get_events()
        for event in device_events:
            print(f"Device event: {event}")
        
        # Выполняем инструкции CPU
        if cpu.running:
            cpu.step()
        
        # Обновляем и отрисовываем устройства
        device_manager.update()
        device_manager.draw()
        
        # Ограничиваем FPS
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    