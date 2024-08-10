import os #для работы с операционной системой
import unicurses as curses # библиотека для работы с консолью

from arcanoid import get_game_params, MAPS_PATH, SCREENS_PATH
from arcanoid.map import Map # импортируем класс карты
from arcanoid.utils import read_map_from_file #функция для получения символов из файла
from arcanoid.color_themes import (init_color_themes, 
                                   PLATFORM_DESC_COLOR, BALL_COLOR, BRICK_TYPE_1_COLOR, BRICK_TYPE_2_COLOR, BRICK_TYPE_3_COLOR) #импортируем цвета для разных объектов

bricks_colors = (BRICK_TYPE_1_COLOR, BRICK_TYPE_2_COLOR, BRICK_TYPE_3_COLOR) # цвета для кирпичей
game_params = get_game_params() #получаем параметры игры

def redraw_screen(game_map: Map) -> None:
    """
    Перерисовывает экран, если есть изменения на карте.

    Args:
        game_map (Map): Объект карты.
    """
    if game_map.check_for_change(): #проверяем, изменилась ли карта (двинулось ли что-то на экране)
        curses.erase() #очищаем консоль
        curses.move(game_map.platform_desk.y, game_map.platform_desk.x) #переходим на нужную позицию для отрисовки платформы
        curses.addstr(str(game_map.platform_desk), PLATFORM_DESC_COLOR) #выводим на экран симвоьное обозначение платформы, придавая ей свой цвет
        for counter, brick in enumerate(game_map.bricks): # проходим по списку кирпичей
            curses.move(brick.y, brick.x) #переходим на позицию кирпича
            curses.addch(str(brick), bricks_colors[counter%len(bricks_colors)]) #выводим символ кирпича в консоль с одним из 3 кирпичных цветов.
        for ball in game_map.balls: #проходим по списку мячей (пока в игре лишь один мяч. Задел на будущее развитие)
            curses.move(ball.y, ball.x) #переходим к позиции мяча
            curses.addch(str(ball), BALL_COLOR) #выводим символ мяча в консоль
        curses.refresh() #обновляем экран

def check_for_small_screen(stdscr) -> None:
    """
    Блокирует игру, пока терминал не будет расширен до минимальных размеров, установленных в конфигурациях игры.
    """
    is_changed = False #флаг, показывающий, изменились ли размеры экрана ниже положенного
    height, width = curses.getmaxyx(stdscr) #получаем размеры терминала
    while height<game_params["min_game_height"] or width<game_params["min_game_width"]: #пока размеры меньше, чем надо
        is_changed = True #если мы вошли в этот цикл, значит экран меньше нужного
        curses.clear()  #очищаем экран
        curses.addstr("Для продолжения игры расширьте окно") # выводим строку на экран
        curses.refresh() #обновляем экран
        curses.napms(100) # задержка
        height, width = curses.getmaxyx(stdscr) # получаем размеры терминала
    return is_changed

def select_level(stdscr) -> str:
    """Функция для показа экрана выбора уровня"""
    files = os.listdir(MAPS_PATH) #получаем список файлов в директории с уровнями
    if not len(files): # если файлов в директории нет
        raise Exception("Отсутствует директория с картами") # инициируем исключение
    current_pos = 0 # индекс в списке файлов
    symbols = read_map_from_file(SCREENS_PATH+"logo.txt") # получаем список символов из файла лого
    is_changed = True #флаг для оптимизации. Чтобы не перерисовывало экран, если мы ничего не нажали
    while True: #бесконечный цикл
        is_changed = check_for_small_screen(stdscr) or is_changed #проверяем на минимальный экран
        if is_changed: # если была нажата кнопка
            curses.erase() #очищаем экран
            for symbol in symbols: #проходим по символам из лого
                curses.move(symbol.y, symbol.x) #двигаемся на позицию символа
                curses.addch(symbol.sym) #печатаем символ
            curses.move(12, 64) #опускаемся пониже
            curses.addstr("Выберите уровень") # выводим надпись

            curses.move(14, 64) #опускаемся пониже
            curses.addstr(f"-> {files[current_pos].strip('.txt')}") # выводим надпись с названием уровня
         
            curses.refresh() #обновляем экран
            is_changed = False #говорим, чтобы не обновляло экран
        
        key = curses.getch() #пытаемся считать нажатие кнопки
        if key in (curses.KEY_LEFT, curses.KEY_UP): #если нажата стрелка вверх или влево
            current_pos = (current_pos-1)%len(files) #уменьшаем индекс уровня
            is_changed = True                        # говорим, что надо экран перерисовать
        elif key in (curses.KEY_RIGHT, curses.KEY_DOWN): #если нажата стрелка вниз или вправо
            current_pos = (current_pos+1)%len(files) #увеличиваем индекс уровня
            is_changed = True # говорим, что надо экран перерисовать
        elif key == ord("\n"): #если нажали enter, значит выбрали уровень
            return MAPS_PATH+files[current_pos] #вернули путь до файла выбранного уровня (вышли из вечного цикла)
        curses.flushinp() #очистка буфера ввода
        curses.napms(100) #задержка
        


def main(stdscr) -> None:
    """
    Основная функция игры.
    """
    curses.start_color() # говорим, что в консоли можно использовать разные цвета
    init_color_themes() # Инициируем цветовые схемы для разны объектов
    curses.curs_set(0) # делаем курсор невидимым
    curses.noecho() # говорим, чтобы при нажатии на клавиши, они не печатались в консоли
    curses.cbreak() # включаем режим с немедленной обработкой нажатия клавиш
    curses.nodelay(stdscr, True) # позволяет использовать getch без блокирования программы
    curses.keypad(stdscr, True) # Позволяет считывать специальные клавиши, такие как стрелки
    
    while True: #цикл игры
        level_file = select_level(stdscr) #получаем путь к файлу уровня
        game_map = Map(level_file) # создаём объект карты
        game_map.initialize_platform() # создаём платформу

        while len(game_map.balls)>0 and len(game_map.bricks)>0: # Цикл непосредственно игры. Игра не завершится, пока есть хоть один мяч или хоть один кирпич
            check_for_small_screen(stdscr) # проверка на маленькое окно

            key = curses.getch() # пытаемся считать нажатие клавиши
            if key == curses.KEY_RESIZE: # если окно изменило размер 
                game_map.resize(*curses.getmaxyx(stdscr)[::-1]) # меняем размеры игровой области в карте
            if key == ord(' '): # если нажат пробел (функция ord - возвращает код символа)
                game_map.launch_ball() # то запускаем мяч с платформы
            if key in [ord('a'), ord('A'), curses.KEY_LEFT]: # Если нажата клавиша a(английская) или стрелка <-
                game_map.platform_desk.move(-1) # то двигаем платформу влево
            if key in [ord('d'), ord('D'), curses.KEY_RIGHT]: # если клавиша d или стрелка ->
                game_map.platform_desk.move(1) # то двигаем платформу вправо

            curses.flushinp() # очищаем буффер ввода
            game_map.move_balls() # двигаем мячи на один ход
            redraw_screen(game_map) # перерисовываем экран
            
            curses.napms(10) #задержка на 10 мс

        #тут мы вышли из цикла (проиграли или выиграли)
        #считали символы из соответствующего файла
        symbols = read_map_from_file(SCREENS_PATH+("victory.txt" if game_map.balls else "game_over.txt"))
        while True: # цикл постигрового экрана
            check_for_small_screen(stdscr) #проверяем размеры
            curses.erase() #очищаем экран
            for symbol in symbols: #печатаем символы
                curses.move(symbol.y, symbol.x)
                curses.addch(symbol.sym)
            curses.move(12, 64) #двигаемся ниже
            curses.addstr("Нажмите enter") #выводим надпись
            curses.refresh() #обновляем экран
    
            key = curses.getch() #пытаемся отследить нажатие клавиш
            if key == ord("\n"): #если нажали enter
                break   #то выходим из цикла и попадаем в самое начало первого цикла
            curses.flushinp() #очищаем буфер ввода
            curses.napms(100) #задержка
