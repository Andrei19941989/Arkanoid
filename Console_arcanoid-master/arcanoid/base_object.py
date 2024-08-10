class BaseObject:
    """класс объекта на карте"""
    def __init__(self, x: int, y: int, sym: str):
        """
        Инициирует объект
        
        Args:
            x (int): x-координата.
            y (int): y-координата.
            sym (str): символ объекта.
        """
        self.x = x
        self.y = y
        self.sym = sym
        self.observer = None #для наблюдателя

    def __str__(self):
        """
        Возвращает строковое представление объекта. Вызывается при приведении объекта к типу str.

        Returns:
            str: строковое представление объекта.
        """
        return self.sym
    
    def get_pixels_coordinates(self) -> tuple[int, int]:
        """
        Возвращает координаты символа кирпича.

        Returns:
            tuple[int, int]: кортеж, представляющий координаты символа кирпича: (x, y).
        """
        return(self.x, self.y)
    
    def add_observer(self, observer) -> None:
        """
        Инициирует наблюдателя за объектом.

        Args:
            observer (Map): наблюдатель - экземпляр класса Map.
        """
        self.observer = observer