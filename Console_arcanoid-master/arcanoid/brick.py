from arcanoid.base_object import BaseObject

class Brick(BaseObject):
    """Класс кирпича"""
    def __init__(self, x: int, y: int):
        """
        Создаёт экземпляр кирпича.

        Args:
            x (int): x-координата кирпича.
            y (int): y-координата кирпича.
        """
        super().__init__(x, y, "#") #вызов конструктора родительского класса
    
    def has_pixel(self, x: int, y: int) -> bool:
        """
        Проверяет, располагается ли 'пиксель' с координатами (x, y) к данному объекту.

        Args:
            x (int): x-координата пикселя.
            y (int): y-координата пикселя.

        Returns:
            bool: True, если пиксель (x,y) относится к данному кирпичу, иначе False.
        """
        return self.x==x and self.y==y