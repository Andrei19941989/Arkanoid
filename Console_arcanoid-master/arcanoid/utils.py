from collections import namedtuple #импортируем именованный кортеж
#отличия от обычного кортежа:
#доступ к элементам обычного кортежа - по индексам. Например, symbol[0]
#У именованного кортежа через точечную нотацию (как поля класса). symbol.x
Symbol = namedtuple("Symbol", ['sym', 'x', 'y']) #регистрируем "класс" кортежа.
#Это "класс" Symbol, который содержит поля x, y, sym

def read_map_from_file(filename: str) -> list[tuple[str, int, int]]:
    """
    Читает файл filename и возвращает список с информацией о каждом непробельном символе.

    Args:
        filename (str): путь к файлу.

    Returns:
        list[tuple[str, int, int]]: список именованных кортежей, содержащих поля sym (сам символ), x, y (координаты символа)
    """
    symbols = [] #список символов
    with open(filename, encoding="utf-8") as file: #открываем файл
        for y_index, line in enumerate(file): # считываем строки
            for x_index, sym in enumerate(line): # считываем по символу в строке
                    if sym != " ": # если символ не пробельный
                        symbols.append(Symbol(sym, x_index, y_index)) # то добавляем в список кортеж этого символа
    return symbols #возвращаем список символов