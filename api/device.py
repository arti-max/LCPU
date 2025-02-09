import pygame
from abc import ABC, abstractmethod
import json
import os
import time

class Device(ABC):
    def __init__(self):
        # Базовые атрибуты
        self._value = 0x00
        self._surface = None
        self._rect = None
        self._config = None
        self._enabled = True  # Устройство включено/выключено
        self._last_update = 0  # Время последнего обновления
        self._update_rate = 0  # Частота обновления (0 = без ограничений)
        self._events = []  # Очередь событий устройства
        self._cpu = None  # Добавим ссылку на процессор
        
        # Базовые настройки конфига
        self._default_config = {
            "position": {"x": 100, "y": 100},
            "size": 50,
            "visible": True,
            "enabled": True,
            "update_rate": 0,  # Гц (0 = максимальная)
            "debug": False     # Режим отладки
        }
        
        # Дополнительные настройки, специфичные для конкретного девайса
        self._device_config = {}
        
    def enable(self):
        """Включить устройство"""
        self._enabled = True
        
    def disable(self):
        """Выключить устройство"""
        self._enabled = False
        
    def is_enabled(self):
        """Проверить, включено ли устройство"""
        return self._enabled
    
    def set_update_rate(self, hz):
        """Установить частоту обновления устройства"""
        self._update_rate = hz
        
    def should_update(self):
        """Проверить, нужно ли обновлять устройство"""
        if self._update_rate == 0:
            return True
            
        current_time = time.time()
        if current_time - self._last_update >= 1.0 / self._update_rate:
            self._last_update = current_time
            return True
        return False
    
    def push_event(self, event_type, data=None):
        """Добавить событие в очередь устройства"""
        self._events.append({"type": event_type, "data": data, "time": time.time()})
        
    def get_events(self):
        """Получить все события устройства"""
        events = self._events.copy()
        self._events.clear()
        return events
    
    def handle_event(self, event):
        """Обработать pygame событие"""
        if self._enabled and self._rect and event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self.on_click(event)
    
    def on_click(self, event):
        """Обработчик клика по устройству"""
        pass
    
    def get_debug_info(self):
        """Получить отладочную информацию"""
        if not self._config.get("debug", False):
            return None
            
        return {
            "type": self.__class__.__name__,
            "enabled": self._enabled,
            "value": self._value,
            "position": (self._rect.x, self._rect.y) if self._rect else None,
            "size": (self._rect.width, self._rect.height) if self._rect else None,
            "update_rate": self._update_rate,
            "last_update": self._last_update,
            "events": len(self._events)
        }
    
    def draw_debug(self, screen):
        """Отрисовка отладочной информации"""
        if not self._config.get("debug", False) or not self._rect:
            return
            
        # Рисуем рамку вокруг устройства
        pygame.draw.rect(screen, (255, 0, 0), self._rect, 1)
        
        # Отображаем основную информацию
        font = pygame.font.Font(None, 24)
        debug_text = f"{self.__class__.__name__}: {hex(self._value)}"
        text_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(text_surface, (self._rect.x, self._rect.y - 20))
    
    def draw(self, screen):
        """Отрисовка устройства с поддержкой отладки"""
        if self._surface and self._rect and self._config.get("visible", True):
            screen.blit(self._surface, self._rect)
            if self._config.get("debug", False):
                self.draw_debug(screen)
    
    def get_default_config(self):
        """Получить конфигурацию по умолчанию"""
        # Объединяем базовые настройки с настройками девайса
        config = self._default_config.copy()
        config.update(self._device_config)
        return config
        
    def deep_update(self, target, source):
        """Рекурсивно обновляет словарь, добавляя отсутствующие поля"""
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    # Рекурсивно обновляем вложенные словари
                    self.deep_update(target[key], value)
                # Если значение уже существует, оставляем пользовательское
            else:
                # Если поля нет, добавляем из дефолтного конфига
                target[key] = value

    def load_config(self, config_path):
        """Загрузка или создание конфигурации девайса"""
        try:
            # Получаем дефолтный конфиг
            self._config = self.get_default_config()
            
            # Пытаемся загрузить существующий конфиг
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    
                # Обновляем конфиг, сохраняя существующие значения и добавляя новые поля
                self.deep_update(user_config, self._config)
                self._config = user_config
                
                # Сохраняем обновленный конфиг
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(self._config, f, indent=4)
                    
            else:
                # Если конфига нет, создаём новый
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(self._config, f, indent=4)
                print(f"Создан новый конфиг: {config_path}")
                
        except Exception as e:
            print(f"Ошибка при работе с конфигом {config_path}: {e}")
            self._config = self.get_default_config()
            
    def save_config(self, config_path):
        """Сохранение текущей конфигурации в файл"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении конфига {config_path}: {e}")
        
    @abstractmethod
    def IN(self):
        """Получить значение от устройства"""
        if not self._enabled:
            return 0x00
        return self._value
        
    @abstractmethod
    def OUT(self, value):
        """Отправить значение устройству"""
        if self._enabled:
            self._value = value
        
    def get_surface(self):
        """Получить поверхность для отрисовки"""
        return self._surface
        
    def update(self):
        """Обновление состояния устройства"""
        if not self._enabled or not self.should_update():
            return
        
        # Обновление состояния девайса
        pass

    def set_cpu(self, cpu):
        """Устанавливаем процессор для доступа к его методам"""
        self._cpu = cpu

    def is_running(self):
        """Проверяет, запущен ли процессор"""
        if self._cpu:
            return self._cpu.running
        return False

    def set_running(self, state):
        """Устанавливает состояние процессора (запущен/остановлен)"""
        if self._cpu:
            self._cpu.running = state 