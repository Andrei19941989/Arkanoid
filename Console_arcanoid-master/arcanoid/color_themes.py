import unicurses as curses # библиотека для работы с консолью

__PLATFORM_DESC = 1 #константа для платформы
__BALL = 2 #константа для мяча
__BRICK_1 = 3 # первая константа для кирпича
__BRICK_2 = 4 # вторая константа для кирпича
__BRICK_3 = 5 # третья константа для кирпича

def init_color_themes() -> None:
    """
    Инициирует цветовые пары для разных элементов игры, таких, как платформа, кирпичи, мячи.
    """
    curses.init_pair(__PLATFORM_DESC, curses.COLOR_YELLOW, curses.COLOR_BLACK) #инициализирует цветовую пару (жёлтый цвет символа, чёрный цвет фона). Эта пара будет доступна по константе для платформы.
    curses.init_pair(__BALL, curses.COLOR_WHITE, curses.COLOR_BLACK) # аналогично для других объектов
    curses.init_pair(__BRICK_1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(__BRICK_2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(__BRICK_3, curses.COLOR_BLUE, curses.COLOR_BLACK)

PLATFORM_DESC_COLOR = curses.color_pair(__PLATFORM_DESC) #константа цвета платформы. При добавлении строки (или символа) в консоль, нужно указать эту константу, чтобы выводимые символы были нужного цвета.
BALL_COLOR = curses.color_pair(__BALL) #аналогично для других объектов
BRICK_TYPE_1_COLOR = curses.color_pair(__BRICK_1)
BRICK_TYPE_2_COLOR = curses.color_pair(__BRICK_2)
BRICK_TYPE_3_COLOR = curses.color_pair(__BRICK_3)