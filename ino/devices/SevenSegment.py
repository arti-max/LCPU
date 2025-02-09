from api.device import Device
import pygame

class SevenSegment(Device):
    def __init__(self):
        super().__init__()
        
        # Настройки индикатора
        self._device_config = {
            "colors": {
                "on": [255, 50, 50],   # Цвет включённых сегментов
                "off": [50, 0, 0],     # Цвет выключенных сегментов
                "border": [80, 80, 80] # Цвет рамки
            },
            "size": 20,                # Размер сегментов
            "position": {
                "x": 400,              # Позиция по X
                "y": 100               # Позиция по Y
            }
        }
        
        self._size = self._device_config["size"]
        self._surface = pygame.Surface((self._size * 3, self._size * 5), pygame.SRCALPHA)
        self._rect = pygame.Rect(
            self._device_config["position"]["x"],
            self._device_config["position"]["y"],
            self._size * 3,
            self._size * 5
        )
        self._value = 0  # Текущее значение
        
    def IN(self):
        """Индикатор не возвращает значение процессору"""
        return 0x00
        
    def OUT(self, value):
        """Устанавливает значение для отображения"""
        self._value = value % 10  # Ограничиваем значение от 0 до 9
        
    def update(self):
        """Обновление отображения индикатора"""
        if not self._config:
            return
            
        # Очищаем поверхность
        self._surface.fill((0, 0, 0, 0))
        
        # Сегменты индикатора (a, b, c, d, e, f, g)
        segments = [
            (1, 0, 1, 1, 0, 1, 1),  # 0
            (0, 0, 1, 0, 0, 0, 1),  # 1
            (1, 1, 1, 0, 1, 0, 1),  # 2
            (1, 1, 1, 0, 0, 0, 1),  # 3
            (0, 1, 1, 1, 0, 0, 1),  # 4
            (1, 1, 0, 1, 0, 0, 1),  # 5
            (1, 1, 0, 1, 1, 0, 1),  # 6
            (1, 0, 1, 0, 0, 0, 1),  # 7
            (1, 1, 1, 1, 1, 0, 1),  # 8
            (1, 1, 1, 1, 0, 0, 1)   # 9
        ]
        
        # Рисуем сегменты
        segment_coords = [
            (1, 0, 1, 0),  # a
            (2, 1, 0, 1),  # b
            (2, 3, 0, 1),  # c
            (1, 4, 1, 0),  # d
            (0, 3, 0, 1),  # e
            (0, 1, 0, 1),  # f
            (1, 2, 1, 0)   # g
        ]
        
        for i, (x, y, w, h) in enumerate(segment_coords):
            color = self._config["colors"]["on"] if segments[self._value][i] else self._config["colors"]["off"]
            pygame.draw.rect(self._surface, color, 
                             (x * self._size, y * self._size, 
                              w * self._size + self._size, h * self._size + self._size))