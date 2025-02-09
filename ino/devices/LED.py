from api.device import Device
import pygame

class LED(Device):
    def __init__(self):
        super().__init__()
        
        # Настройки LED
        self._device_config = {
            "colors": {
                "on": [255, 50, 50],     # Более мягкий красный для включенного состояния
                "off": [50, 0, 0],        # Более тёмный для выключенного
                "glow": [255, 100, 100],  # Цвет свечения
                "border": [80, 80, 80]    # Цвет рамки
            },
            "size": 30,                   # Размер светодиода
            "border": 2,                  # Толщина рамки
            "glow_radius": 5,             # Радиус свечения
            "position": {
                "x": 750,                 # Позиция по X
                "y": 550                  # Позиция по Y
            }
        }
        
        self._size = self._device_config["size"]
        self._surface = pygame.Surface((self._size * 2, self._size * 2), pygame.SRCALPHA)
        self._rect = pygame.Rect(
            self._device_config["position"]["x"],
            self._device_config["position"]["y"],
            self._size * 2,
            self._size * 2
        )
        self._state = False
        
    def IN(self):
        """Возвращает текущее состояние светодиода"""
        return 0x01 if self._state else 0x00
        
    def OUT(self, value):
        """Устанавливает состояние светодиода"""
        self._state = value
        
    def update(self):
        """Обновление отображения с эффектом свечения"""
        if not self._config:
            return
            
        # Очищаем поверхность
        self._surface.fill((0, 0, 0, 0))
        
        center = (self._size, self._size)
        
        if self._state:
            # Рисуем свечение (только когда включен)
            glow_color = self._config["colors"]["glow"]
            for radius in range(self._config["glow_radius"], 0, -1):
                alpha = 100 - (radius * 20)
                color = (*glow_color, alpha)
                pygame.draw.circle(self._surface, color, center, 
                                 self._size//2 + radius)
        
        # Рисуем рамку
        pygame.draw.circle(self._surface, self._config["colors"]["border"], center,
                         self._size//2)
        
        # Рисуем основной круг
        color = self._config["colors"]["on"] if self._state else self._config["colors"]["off"]
        pygame.draw.circle(self._surface, color, center,
                         self._size//2 - self._config["border"])
        
        # Добавляем блик
        if self._state:
            highlight_pos = (center[0] - self._size//4, center[1] - self._size//4)
            pygame.draw.circle(self._surface, (255, 255, 255, 150),
                             highlight_pos, self._size//8)
        
    def load_config(self, config_path):
        super().load_config(config_path)
        if self._config:
            if 'position' in self._config:
                self._rect.x = self._config['position']['x']
                self._rect.y = self._config['position']['y']
            if 'size' in self._config:
                self._size = self._config['size']
                self._surface = pygame.Surface((self._size * 2, self._size * 2), pygame.SRCALPHA)
                self._rect.width = self._size * 2
                self._rect.height = self._size * 2

    def on_click(self, event):
        if self._config["interaction"]["clickable"]:
            if self._config["interaction"]["toggle"]:
                self._state = not self._state  # Переключаем состояние
                self._value = 1 if self._state else 0  # Обновляем значение
                self.push_event("toggle", self._value)
                print(f"LED clicked: state = {self._state}, value = {self._value}")