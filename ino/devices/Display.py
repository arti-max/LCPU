from api.device import Device
import pygame
import numpy as np

class Display(Device):
    def __init__(self):
        super().__init__()
        
        # Настройки дисплея
        self._device_config = {
            "size": {
                "width": 16,    # Размер в пикселях
                "height": 16,
                "pixel": 15     # Увеличили размер пикселя
            },
            "colors": {
                "off": [0, 15, 0],      # Сделали темнее
                "on": [0, 255, 0],      # Ярко-зелёный для включенных
                "border": [50, 50, 50],  # Сделали темнее
                "button": [45, 45, 45],  # Цвет кнопки
                "button_pressed": [40, 40, 40]  # Цвет нажатой кнопки
            },
            "position": {
                "x": 50,
                "y": 50
            },
            "margin": 10,      # Уменьшили отступ
            "button": {
                "width": 40,   # Ширина кнопки
                "height": 25,  # Высота кнопки
                "margin": 15,  # Увеличили отступ от экрана
                "offset": 5    # Дополнительный отступ слева
            }
        }
        
        # Инициализация буфера дисплея
        self._buffer = np.zeros((16, 16), dtype=np.uint8)
        self._input_state = 0
        self._current_brightness = 0
        self._current_x = 0
        self._button_pressed = False
        
        # Создание поверхности
        screen_width = self._device_config["size"]["width"] * self._device_config["size"]["pixel"] + self._device_config["margin"] * 2
        screen_height = self._device_config["size"]["height"] * self._device_config["size"]["pixel"] + self._device_config["margin"] * 2
        
        # Добавляем место для кнопки справа
        total_width = screen_width + self._device_config["button"]["margin"] + self._device_config["button"]["width"]
        total_height = screen_height + 10
        
        self._surface = pygame.Surface((total_width, total_height))
        self._rect = pygame.Rect(
            self._device_config["position"]["x"],
            self._device_config["position"]["y"],
            total_width,
            total_height
        )
        
        # Область кнопки CLS (справа от экрана)
        self._cls_button = pygame.Rect(
            screen_width + self._device_config["button"]["offset"],  # Добавили отступ слева
            (total_height - self._device_config["button"]["height"]) // 2,
            self._device_config["button"]["width"],
            self._device_config["button"]["height"]
        )
        
        # Добавляем имя устройства
        self.name = "Base Display 16x16"  # Укажите нужное имя устройства
        
    def IN(self):
        """Дисплей не поддерживает чтение"""
        return 0x00
        
    def OUT(self, value):
        """Обработка входящих данных"""
        if self._input_state == 0:  # Получаем яркость
            self._current_brightness = value
            self._input_state = 1
        elif self._input_state == 1:  # Получаем X
            self._current_x = value
            self._input_state = 2
        elif self._input_state == 2:  # Получаем Y и устанавливаем пиксель
            self._buffer[value % 16][self._current_x % 16] = self._current_brightness
            self._input_state = 0
            
    def clear_screen(self):
        """Очистка экрана"""
        self._buffer.fill(0)
        
    def handle_event(self, event):
        """Обработка нажатия на кнопку CLS"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self._cls_button.collidepoint(mouse_pos):
                self._button_pressed = True
                self.clear_screen()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._button_pressed = False

    def draw_ui(self):
        # Рисуем кнопку CLS с учетом состояния
        button_color = self._config["colors"]["button_pressed"] if self._button_pressed else self._config["colors"]["button"]
        pygame.draw.rect(self._surface, button_color, self._cls_button)
        
        # Добавляем текст на кнопку
        font = pygame.font.Font(None, 20)
        text = font.render("CLR", True, (200, 200, 200))
        text_rect = text.get_rect(center=self._cls_button.center)
        self._surface.blit(text, text_rect)

        # Отображаем имя устройства под дисплеем
        name_font = pygame.font.Font(None, 24)
        name_text = name_font.render(self.name, True, (255, 255, 255))  # Белый цвет
        name_rect = name_text.get_rect(center=(self._surface.get_width() // 3.6, self._surface.get_height() - 10))  # Центрируем под дисплеем
        self._surface.blit(name_text, name_rect)
        
    def update(self):
        """Обновление состояния дисплея"""


        if not self.is_running():
            # Если процессор остановлен, очищаем буфер дисплея
            self._buffer.fill(0)  # Устанавливаем все пиксели в 0 (выключены)
            self._surface.fill(self._config["colors"]["border"])  # Заполняем фон
            
            # Рисуем пиксели
            pixel_size = self._config["size"]["pixel"]
            margin = self._config["margin"]

            for y in range(16):
                for x in range(16):
                    color = self._config["colors"]["off"]
                    pygame.draw.rect(self._surface, color,
                    (margin + x * pixel_size,
                     margin + y * pixel_size,
                     pixel_size - 1,
                     pixel_size - 1)
                )
                    
            self.draw_ui()
            return  # Выходим из метода, чтобы не выполнять дальнейшую отрисовку

        # Если процессор запущен, продолжаем обычное обновление
        self._surface.fill(self._config["colors"]["border"])
        
        # Рисуем пиксели
        pixel_size = self._config["size"]["pixel"]
        margin = self._config["margin"]
        
        for y in range(16):
            for x in range(16):
                brightness = self._buffer[y][x]
                if brightness > 0:
                    color = [
                        int(self._config["colors"]["off"][i] + 
                            (self._config["colors"]["on"][i] - self._config["colors"]["off"][i]) 
                            * brightness / 255)
                        for i in range(3)
                    ]
                else:
                    color = self._config["colors"]["off"]
                    
                pygame.draw.rect(self._surface, color,
                    (margin + x * pixel_size,
                     margin + y * pixel_size,
                     pixel_size - 1,
                     pixel_size - 1)
                )

        self.draw_ui()