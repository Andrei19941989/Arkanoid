import json # библиотека для работы с json файлами

from arcanoid.ball import Ball # импортируем класс мяча
from arcanoid.brick import Brick # импортируем класс кирпича
from arcanoid.platform_desk import PlatformDesk #импортируем класс платформы

__all__ = ["Ball", "Brick", "PlatformDesk"] #нужно, чтобы можно было писать from Arcanoid import Ball вместо from Arcanoid.ball import Ball
MAPS_PATH = "./maps/" #путь к директории с уровнями
SCREENS_PATH = "./game_screens/" #путь к директории с файлами лого и конца игры

def get_game_params() -> dict:
    """
    Считывает параметры игры из файла конфигурации и возвращает их.

    Returns:
        dict: словарь, где ключи - название параметра, а значение - значение параметра.
    """
    CONFIG_PATH = "./configs.json" #путь к файлу конфигурации
    with open(CONFIG_PATH, encoding="utf-8") as file:#открываем файл
        configs = json.load(file) #считываем настройки
    
    configs["ball_speed"] = max(12 - min(configs.get("ball_speed", 2), 10), 2) # пытаемся получить скорость мяча. Устанавливаем минимум на 2, максимум на 10
    configs["platform_size"] = configs.get("platform_size", 11) # Пытаемся получить размер платформы. Если не получается, то устанавливаем в 11
    configs["platform_speed"] = configs.get("platform_speed", 1) #Пытаемся получить скорость платформы
    configs["min_game_width"] = configs.get("min_game_width", 150) #Пытаемся получить ширину игрового пространства
    configs["min_game_height"] = configs.get("min_game_height", 40) #Пытаемся получить высоту игрового пространства

    return configs