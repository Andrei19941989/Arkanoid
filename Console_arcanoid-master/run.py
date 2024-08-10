import unicurses as curses # библиотека для работы с консолью
from arcanoid.screen import main # основная функция игры

curses.wrapper(main) #запускаем функцию игры в обёртке консоли