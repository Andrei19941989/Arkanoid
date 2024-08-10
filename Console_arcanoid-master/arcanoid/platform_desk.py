from arcanoid.base_object import BaseObject

class PlatformDesk(BaseObject):
    """Класс платформы"""
    def __init__(self, x, y, size=11, speed=1):
        """
        Создаёт экземпляр платформы.

        Args:
            x (int): x-координата левого края платформы.
            y (int): y-координата платформы.
            size (int, optional): Размер платформы в символах. По умолчанию 11.
            speed (int, optional): количество символов, которое платформа пройдёт за одно движение. По умолчанию 1.
        """
        super().__init__(x, y, "=") #вызов конструктора родительского класса.
        self.size=size
        self.speed=speed
        self.has_ball = True #флаг, показывающий, что мяч прикреплён к платформе.
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта. Вызывается при приведении объекта к типу str.

        Returns:
            str: строковое представление объекта.
        """
        return self.sym*self.size

    def move(self, dx: int) -> None:
        """
        Метод движения платформы. Изменяет координаты платформы и уведомляет наблюдателя о смене положения.

        Args:
            dx (int): направление движения: 1 - вправо, -1 - влево.
            max_limit (int): x-координата правой стенки игровой области.
        """
        if self.x+dx>=0 and self.x+dx+self.size<=self.observer.xlim: # если при движении платформы выходим за пределы экрана
            for _ in range(self.speed): #возможны ситуации, когда при скорости, например, 3, от края платформы до стены расстояние в 1 символ
                #тогда при попытке сдвинуться платформа выйдет за границу. Поэтому мы будем двигать платформу на 1 символ, но 3 раза.
                if self.x+dx>=0 and self.x+dx+self.size<=self.observer.xlim: #если при попытке сдвинуть на 1 символ платформа НЕ выходит за границы
                    self.x+=dx #то двигаем платформу
            self.observer.notice(self) #после перемещения уведомляем наблюдателя

    def change_y_pos(self, y: int) -> None:
        """
        Перемещает платформу по оси OY. Изменяет y-координату платформы и уведомляет наблюдателя о смене положения.
        
        Args:
            y (int): новая y-координата платформы.
        """
        self.y = y #заменяем координату y
        self.observer.notice(self) #уведомляем наблюдателя

    def launch(self) -> None:
        """
        Метод, инициирующий запуск мяча с платформы.
        """
        if self.has_ball:
            self.has_ball = False

    def get_pixels_coordinates(self) -> list[tuple[int, int]]:
        """
        Возвращает список координат каждого символа платформы.

        Returns:
            list[tuple[int, int]]: список кортежей, представляющих координаты символа платформы: (x, y).
        """
        return [(self.x+shift, self.y) for shift in range(self.size)]