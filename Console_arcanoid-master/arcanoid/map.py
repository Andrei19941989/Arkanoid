import random #импорт модуля для случайности

from arcanoid import get_game_params, Ball, Brick, PlatformDesk

class Map:
    """Класс карты (контроллер движений элементов)"""
    def __init__(self, level_file: str):
        """
        Создаёт экземпляр контроллера.

        Args:
            level_file(str): путь к файлу уровня.
        """
        self.game_params = get_game_params() #параметры игры
        self.xlim=self.game_params["min_game_width"] #граница по x
        self.ylim=self.game_params["min_game_height"] #граница по y
        self.platform_desk=None #для платформы
        self.balls = [] #список мячей
        self.bricks = [] #список кирпичей
        self.active_pixels={} #словарь пикселей (координаты символов в консоли)
        self.is_changed = False # флаг, показывающий, было ли совершено движение в игре после последней проверки
        self._initialize_bricks(level_file) #выстраивание кирпичей на карте

    def check_for_change(self) -> bool:
        """
        Проверяет, изменилось ли положения каких-либо объектов.
        
        Returns:
            bool: True, если произошло неотслеженное движение каких-либо объектов, иначе False.
        """
        if self.is_changed: #если кто-то двинулся
            self.is_changed=False   #то опускаем флаг
            return True #и возвращаем True
        return False #иначе False

    def initialize_platform(self) -> None:
        """
        Инициализирует платформу с мячом на ней и начинает их отслеживание.
        """
        self.platform_desk = PlatformDesk(self.xlim//2-self.game_params["platform_size"]//2, # ставит платформу снизу по центру
                                          self.ylim-2,
                                          size=self.game_params["platform_size"],  #указывается размер и скорость из параметров игры
                                          speed=self.game_params["platform_speed"])
        self.balls.append(Ball(self.platform_desk.x+self.platform_desk.size//2,  #создаём мяч, находящийся на центре платформы
                               self.platform_desk.y-1, 
                               self.game_params["ball_speed"])) #указываем скорость мяча из параметров игры
        self.platform_desk.add_observer(self) #инициируем наблюдателя для платформы. Теперь объект Map отслеживает движения платформы.
        self.balls[0].add_observer(self) # такой же наблюдатель для мяча
        self.active_pixels[self.platform_desk] = self.platform_desk.get_pixels_coordinates() #добавляем в словарь для платформы список координат символов, из которых состоит платформа
        self.active_pixels[self.balls[0]] = self.balls[0].get_pixels_coordinates() #то же самое для мяча

    def _initialize_bricks(self, level_file: str) -> None:
        """
        Инициализирует кирпичи, согласно файлу карты уровня.

        Args:
            level_file (str): путь до файла уровня.
        """
        with open(level_file, encoding="utf-8") as file: #открываем файл с уровнем
            for y_index, line in enumerate(file): #проходим по строкам
                for x_index, sym in enumerate(line): #проходим по символам в строке
                    if sym=="#": #если найден символ #
                        self.bricks.append(Brick(x_index, y_index)) #то добавляем в список кирпичей кирпич с координатами равными положению символа в файле уровня
        self.active_pixels["bricks"] = set([brick.get_pixels_coordinates() for brick in self.bricks]) # в словарь для кирпичей добавляем множество, состоящее из координат всех кирпичей


    def resize(self, xlim: int, ylim: int) -> None:
        """
        Изменяет размеры игровой области и перемещает платформу по оси OY.

        Args:
            xlim (int): ширина игровой области в символах.
            ylim (int): высота игровой области в символах. 
        """
        self.xlim = xlim # меняем границы
        self.ylim = ylim
        self.platform_desk.change_y_pos(ylim-2) #меняем положение платформы

    def notice(self, obj):
        """
        Метод уведомления. Вызывается отслеживаемым объектом при изменении своих координат.

        Args:
            obj (Ball | PlatformDesk): Объект мяча или платформы, которые изменили положение.
        """
        self.is_changed=True # если платформа или мяч вызвали этот метод, значит, они переместились.
    
        if obj is self.platform_desk: #если метод был вызван платформой
            pixels = obj.get_pixels_coordinates() #получаем координаты символов платформы
            self.active_pixels[obj] = pixels #обновляем словарь. Вставляем новый набор координат для платформы
            if self.platform_desk.has_ball: #если на платформе ещё находится мяч
                self.balls[0].y = pixels[0][1]-1 #то мяч будет двигаться вместе с платформой
                self.balls[0].x = pixels[(len(pixels)-1)//2][0]
                self.active_pixels[self.balls[0]]=(self.balls[0].x, self.balls[0].y) #обновляем координаты для мяча в словаре
        
        elif obj in self.balls: #если метод вызвал мяч
            self.active_pixels[obj] = (obj.x, obj.y) #получаем координаты мяча
            try: 
                platform_index = self.active_pixels[self.platform_desk].index((obj.x+obj.dx, obj.y+obj.dy)) #пытаемся получаем номер символа на платформе, об который стукнется мяч на своём следующем ходу
                if platform_index/self.platform_desk.size < 0.25: #делим номер этого символа на длину платформы. Если мяч стукнется об самую правую четверть платформы
                    obj.dx= -2 #то мяч отскочит влево и полетит под более острым углом. Каждый ход будет сдвигаться на 2 символа по OX и на 1 символ по OY.
                elif platform_index/self.platform_desk.size < 0.5: #если мяч ударился чуть левее центра
                    obj.dx= -1 #то отлетит влево под углом 45 градусов. Каждый ход будет сдвигаться на 1 символ по OX и на 1 символ по OY.
                elif platform_index/self.platform_desk.size < 0.75: #если мяч ударился чуть правее центра
                    obj.dx= 1 #то отлетит вправо под углом 45 градусов. Каждый ход будет сдвигаться на 1 символ по OX и на 1 символ по OY.
                else: #иначе мяч ударился в самую правую часть платформы.
                    obj.dx= 2 # мяч отскочит вправо и полетит под более острым углом. Каждый ход будет сдвигаться на 2 символа по OX и на 1 символ по OY.
                obj.dy=-abs(obj.dy) #мяч будет лететь вверх
            except ValueError: # если не получилось получить номер символа платформы (значит мяч не литит на платформу)
                pass #то ничего не делаем
            
            #==========================================ниже прописана логика столкновения мяча с кирпичами===========================
            # Мы не можем проверять столкновения с кирпичами так же, как с платформой.
            # вот пример: мяч летит вправо и вверх 
            #
            #   #        #       #O
            #    #  ->   O# ->    #
            #  O 
            # Получается, что мяч прошёл по диагонали через 2 кирпича, которые по идее не должны были этого позволить.
            # Поэтому необходимы дополнительные проверки

            if abs(obj.dx)==1: #если мяч летит под углом 45 градусов
                potential_pixel_x = (obj.x-obj.dx, obj.y) #координата мяча, смещённого назад по OX
                potential_pixel_y = (obj.x, obj.y-obj.dy) #Координата мяча, смещённого назад по OY
                if set([obj.get_pixels_coordinates(), potential_pixel_x, potential_pixel_y]).intersection(self.active_pixels["bricks"]):
                    #если среди кирпичей есть те, на которые попал мяч в текущем положении или мяч, смещённый по какой-либо оси
                    if potential_pixel_x in self.active_pixels["bricks"]: # если, мяч, смещённый по оси OX попадает на кирпич
                        #значит, что произошло поведение, описанное в примере выше. Будем считать, что мяч прежде, чем пройти сквозь  кирпича, сначала ударяется об левый.
                        obj.dy*=-1   # в таком случае он ударился о нижнюю стенку кирпича и отскакивает по оси OY в противоположном направлении 
                        obj.x-=obj.dx # перемещаем мяч на место, где он должен быть на самом деле после столкновения
                        obj.y+=obj.dy
                        self._crush_brick(*potential_pixel_x) #ломаем кирпич, с которым произошло столкновение.

                    elif potential_pixel_y in self.active_pixels["bricks"]: #то же самое, но для правого кирпича
                        obj.dx*=-1 #для нашего примера мяч отскакивает от правой стенки кирпича. И меняет направление по OX.
                        obj.y-=obj.dy # перемещаем мяч на место, где он должен быть на самом деле после столкновения
                        obj.x+=obj.dx 
                        self._crush_brick(*potential_pixel_y) #ломаем кирпич, с которым произошло столкновение.
                    
                    else: #Это тот случай, когда мяч попал по кирпичу идеально, и ему ничего не мешало.
                        obj.dx*=-1 # он как-бы ударился в угол кирпича, поэтому отражаем его движение по обоим осям
                        obj.dy*=-1
                        self._crush_brick(*obj.get_pixels_coordinates()) # ломаем кирпич
            
            elif abs(obj.dx)==2: #То же самое, но для случая, когда мяч летит с dx=2. В целом проверки те же, только проверяется больше кирпичей
                potential_pixel_x_1 = (obj.x-obj.dx//2, obj.y-obj.dy)
                potential_pixel_y = (obj.x-obj.dx//2, obj.y)
                potential_pixel_x_2 = (obj.x, obj.y-obj.dy)
                if set([obj.get_pixels_coordinates(), potential_pixel_x_1, potential_pixel_x_2, potential_pixel_y]).intersection(self.active_pixels["bricks"]):
                    
                    if potential_pixel_x_1 in self.active_pixels["bricks"]:
                        obj.y-=obj.dy
                        obj.x-=obj.dx
                        obj.dx*=-1
                        self._crush_brick(*potential_pixel_x_1)
                    
                    elif potential_pixel_y in self.active_pixels["bricks"]:
                        obj.x-=obj.dx//2
                        obj.y-=obj.dy
                        obj.dy*=-1
                        self._crush_brick(*potential_pixel_y)

                    elif potential_pixel_x_2 in self.active_pixels["bricks"]:
                        obj.y-=obj.dy
                        obj.x-=obj.dx//2
                        obj.dx*=-1
                        self._crush_brick(*potential_pixel_x_2)
                    
                    else:
                        obj.dx*=-1
                        self._crush_brick(*obj.get_pixels_coordinates())


    def _crush_brick(self, x: int, y: int):
        """
        Метод уничтожения кирпича

        Args:
            x (int): _description_
            y (int): _description_
        """
        for brick in self.bricks: #проходим по списку кирпичей
            if brick.has_pixel(x, y): #если нашли нужный кирпич
                self.bricks.remove(brick) #то удаляем его из списка
                self.active_pixels["bricks"].remove((x, y)) #удаляем информацию о кирпиче из словаря
                break


    def launch_ball(self) -> None:
        """
        Метод запуска мяча. Вызывает метод запуска у платформы и задаёт начальное направление мячу.
        """
        self.platform_desk.launch() #запускаем мяч
        for ball in self.balls: #проходим по списку мячей (там всего 1)
            ball.dx = random.choice([-1, 1]) #выбираем случайное направление по dx
            ball.dy = -1 #направление вверх по dy

    def move_balls(self) -> None:
        """
        Метод движения мячей.
        """
        for ball in self.balls: #проходим по каждому мячу
            ball.move(self.xlim, self.ylim) #двигаем его
            if ball.is_dead: #если мяч потерян
                self.active_pixels.pop(ball) #удаляем мяч из словаря
                self.balls.remove(ball) ###удаляем мяч из списка