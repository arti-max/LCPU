import json
import importlib
import pygame
import os

class DeviceManager:
    def __init__(self):
        self._devices = {}
        self._window = None
        pygame.init()
        self.devices = []
        self._cpu = None
        self._load_prog = None
        
        # Настройки кнопки включения процессора
        button_size = 40  # Размер кнопки
        self.cpu_button = pygame.Rect(740, 10, button_size, button_size)  # Позиция и размер кнопки (квадратная)
        self.power_colors = {
            "on": (0, 255, 0),    # Зеленый когда включен
            "off": (255, 0, 0),   # Красный когда выключен
            "border": (100, 100, 100)  # Серая рамка
        }
        self.powered = False  # Состояние питания

    def init_display(self, width=800, height=600):
        """Инициализация основного окна"""
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("LCPU Devices")
        # Устанавливаем тёмно-серый фон
        self._window.fill((30, 30, 30))
        pygame.display.flip()
        
    def load_devices(self):
        """Загрузка устройств из ports.json"""
        try:
            with open('ino/ports.json', 'r') as f:
                ports = json.load(f)
                
            for port, device_file in ports.items():
                if device_file:  # Если порт не пустой
                    try:
                        # Загружаем модуль устройства
                        module = importlib.import_module(f'ino.devices.{device_file[:-3]}')
                        # Получаем класс устройства
                        device_class = getattr(module, device_file[:-3])
                        # Создаем экземпляр
                        device = device_class()
                        # Загружаем конфиг
                        device.load_config(f'ino/conf/{device_file[:-3]}.cfg')
                        # Сохраняем устройство
                        self._devices[int(port)] = device
                        print(f"Устройство {device_file} загружено на порт {port}")
                        self.devices.append(device)
                    except Exception as e:
                        print(f"Ошибка загрузки устройства {device_file}: {e}")
                    
        except FileNotFoundError:
            print("Файл ports.json не найден")
            
    def add_device(self, port, device):
        """Добавляет устройство на указанный порт"""
        self._devices[port] = device
        
    def get_device(self, port):
        """Возвращает устройство по номеру порта"""
        return self._devices.get(port)

    def draw(self):
        """Отрисовка всех устройств"""
        if self._window:
            self._window.fill((30, 30, 30))  # Тёмно-серый фон
            self.draw_cpu_button()
            for device in self._devices.values():
                device.draw(self._window)
            pygame.display.flip()
            
    def draw_cpu_button(self):
        """Отрисовка кнопки включения процессора"""
        # Рисуем рамку кнопки
        pygame.draw.rect(self._window, self.power_colors["border"], 
                         (self.cpu_button.x - 2, self.cpu_button.y - 2, 44, 44), 2)
        
        # Рисуем саму кнопку
        color = self.power_colors["on"] if self._cpu.running else self.power_colors["off"]
        pygame.draw.rect(self._window, color, self.cpu_button)
        
        # Рисуем символ питания
        center = self.cpu_button.center
        radius = 15
        pygame.draw.circle(self._window, (32, 32, 32), center, radius, 2)
        pygame.draw.line(self._window, (32, 32, 32), 
                         (center[0], center[1] - radius // 2),
                         (center[0], center[1] + radius // 2), 2)
        
        #print(f"DRAW CPU BTN: {color}, {center}, {radius}")

    def handle_events(self, events):
        """Обрабатывает события pygame для всех устройств"""
        for event in events:
            # Обработка нажатия на кнопку включения процессора
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик
                    if self.cpu_button.collidepoint(event.pos):
                        self.toggle_cpu()  # Переключаем состояние процессора
            for device in self._devices.values():
                device.handle_event(event)
                
    def get_events(self):
        """Получает события от всех устройств"""
        events = []
        for device in self._devices.values():
            events.extend(device.get_events())
        return events

    def set_cpu(self, cpu):
        """Устанавливаем процессор для всех устройств"""
        for device in self.devices:
            device.set_cpu(cpu)

    def toggle_cpu(self):
        """Переключение состояния процессора"""
        if self._cpu:
            self.powered = not self._cpu.running  # Переключаем состояние
            if self.powered:  # Если процессор включается
                self._cpu.initialize(self._load_prog)  # Сброс состояния процессора
            self._cpu.running = self.powered  # Устанавливаем состояние процессора

    def update(self):
        """Обновление состояния всех устройств"""
        for device in self._devices.values():
            device.update()
        
        # Обновление состояния кнопки
        self.draw_cpu_button()  # Отрисовка кнопки
        pygame.display.flip()   # Обновление окна