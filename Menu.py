import pygame.draw
import pygame.font


class MenuButton(object):

    def __init__(self, x: int, y: int, w: int, h: int, func=lambda: None, color="#ffffff", width=0, text="",
                 text_color="#000000", text_size=50) -> None:
        """
        Кнопка

        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param func: Функция, которую выполняет кнопка при нажатии
        :param color: Цвет кнопки
        :param width: Ширина рамки при отрисовке
        :param text: Текст на кнопке
        :param text_color: Цвет текста на кнопке
        :param text_size: Размер шрифта на кнопке
        """
        if x < 0 or y < 0 or w < 0 or h < 0:
            raise ValueError
        if type(x) != int or type(y) != int or type(w) != int or type(h) != int or type(color) != str \
                or type(text_color) != str or type(text_size) != int or type(text) != str:
            raise TypeError
        if type(func) != type(lambda: None):
            raise TypeError
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func
        self.color = color
        self.width = width
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.enabled = True

    def is_clicked(self, pos: tuple) -> bool:
        """
        Проверка на нажатие кнопки

        :param pos: Кортеж из позиции курсора во время нажатия
        :return: Возвращает True или False в зависимости от результата
        """
        x1, y1 = pos
        if self.x <= x1 <= self.x + self.w:
            if self.y <= y1 <= self.y + self.h:
                return True
        return False

    def on_click(self) -> None:
        """
        Выполняет функцию у кнопки
        """
        if self.enabled:
            eval('self.func()')

    def get_clicked(self, pos: tuple) -> None:
        """
        Если была нажата кнопка, то выполняет её функцию

        :param pos: Позиция курсора в виде кортежа
        """
        if self.is_clicked(pos):
            self.on_click()

    def show(self, screen) -> None:
        """
        Выполняет отрисовку на холсте

        :param screen: pygame-холст
        """
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, self.text_color)
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.x + (self.w - text_w) // 2
        text_y = self.y + (self.h - text_h) // 2
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), self.width)
        screen.blit(text, (text_x, text_y))

    def set_enabled(self, b: bool) -> None:
        """
        Устанавливает состояние кнопки

        :param b: True или False
        """
        self.enabled = b


class MenuButtonList(list):

    def __init__(self, li=None) -> None:
        """
        Объект со всеми кнопками

        :param li: Классический список из уже существующих кнопок
        """
        if li is None:
            li = []
        self.li = li
        super().__init__(self.li)

    def is_clicked(self, pos: tuple) -> list:
        """
        Проверяет выполнение всех кнопок

        :param pos: Позиция курсора в виде кортежа
        :return: Возвращает список нажатых кнопок
        """
        lr = []
        for x in self.li:
            if x.is_clicked(pos):
                lr.append(x)
        return lr

    def on_click(self, li: list) -> None:
        """
        Выполняет встроенную функцию у всех кнопок из списка

        :param li: Список кнопок, которые надо нажать
        """
        for x in li:    
            x.on_click()

    def get_clicked(self, pos: tuple) -> None:
        """
        Выполняет вызов функции у всех нажатых кнопок

        :param pos: Позиция курсора ввиде кортежа
        """
        li = self.is_clicked(pos)
        self.on_click(li)

    def show(self, screen) -> None:
        """
        Выполняет отрисовку всех кнопок

        :param screen: pygame-холст
        """
        for x in self.li:
            x.show(screen)

    def get_list(self) -> list:
        """
        Метод получение списка кнопок

        :return: Список кнопок
        """
        return self.li


class MenuStringLabel(object):

    def __init__(self, x: int, y: int, w: int, h: int, text: str, text_color="#ffffff", text_size=50) -> None:
        """
        Надпись в одну строку

        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param text: Текст
        :param text_color: Цвет текста
        :param text_size: Размер текста
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.text_color = text_color
        self.text_size = text_size

    def show(self, screen) -> None:
        """
        Метод отрисовки надписи в одну строку

        :param screen: Холст
        """
        font = pygame.font.Font(None, self.text_size)
        self.text_text = font.render(self.text, True, self.text_color)
        self.text_w = self.text_text.get_width()
        self.text_h = self.text_text.get_height()
        self.text_x = self.x + (self.w - self.text_w) // 2
        self.text_y = self.y + (self.h - self.text_h) // 2
        screen.blit(self.text_text, (self.text_x, self.text_y))


class MenuLabel(object):

    def __init__(self, x: int, y: int, w: int, h: int, color="#ffffff", width=0, text="",
                 text_color="#000000", text_size=50, indent=5) -> None:
        """
        Надпись

        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param color: Цвет кнопки
        :param width: Ширина рамки при отрисовке
        :param text: Текст на кнопке
        :param text_color: Цвет текста на кнопке
        :param text_size: Размер шрифта на кнопке
        :param indent: Межстроковвый интервал
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.width = width
        self.text = text.split('\n')
        self.text_color = text_color
        self.text_size = text_size
        self.indent = indent

        self.calculation()

    def calculation(self) -> None:
        """
        Метод перерасчета Label'а
        """
        self.li_msl = []

        count = len(self.text)
        c = self.y
        for s in self.text:
            msl = MenuStringLabel(self.x, c, self.w, (self.h - (count - 1) * self.indent) // count, s, self.text_color,
                                  self.text_size)
            self.li_msl.append(msl)
            c += msl.h + self.indent

    def show(self, screen) -> None:
        """
        Метод отрисовки надписи

        :param screen: Холст
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), self.width)
        for msl in self.li_msl:
            msl.show(screen)

    def set_text(self, text: str) -> None:
        """
        Метод для установки текста в надпись

        :param text: Текст для установки
        """
        self.text = text.split('\n')
        self.calculation()


class MenuLabelList(list):

    def __init__(self, li=None) -> None:
        """
        Объект со всеми надписями

        :param li: Классический список из уже существующих кнопок
        """
        if li is None:
            li = []
        self.li = li
        super().__init__(self.li)

    def show(self, screen) -> None:
        """
        Выполняет отрисовку всех надписей

        :param screen: pygame-холст
        """
        for x in self.li:
            x.show(screen)

    def get_list(self) -> list:
        """
        Метод получение списка надписей

        :return: Список кнопок
        """
        return self.li


class MenuLayOut(object):

    def __init__(self, mbl: MenuButtonList, mll: MenuLabelList, place: list, x: int, y: int, w: int, h: int,
                 indent=(10, 10), color="#999999", orientation='v') -> None:
        """
        Элемент интерфейса, с помощью которого можно настраивать меню

        :param mbl: Класс MenuButtonList с кнопками
        :param mll: Класс MenuLabelList с надписями
        :param place: Список с указаниями к расстановке кнопок/надписей b - кнопка, l - надпись
        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param indent: Отступ. Первый элемент - по x, второй - по y
        :param color: Цвет
        :param orientation: Ориентация v - вертикально, h - горизонтально
        """
        self.mbl = mbl
        self.mll = mll
        self.place = place
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.indent = indent
        self.color = color
        self.orientation = orientation

        self.calculation()

    def calculation(self) -> None:
        """
        Метод для расчета размеров
        """
        cb = len(self.mbl)
        cl = len(self.mll)
        if self.orientation == 'v':
            btn_w = self.w - self.indent[0] * 2
            btn_h = self.h // (cb + cl) - self.indent[1] * 2

            def btn_x(n):
                return self.x + self.indent[0]

            def btn_y(n):
                return self.y + self.indent[1] * (2 * n + 1) + n * btn_h
        elif self.orientation == 'h':
            btn_h = self.h - self.indent[1] * 2
            btn_w = self.w // (cb + cl) - self.indent[0] * 2

            def btn_y(n):
                return self.y + self.indent[1]

            def btn_x(n):
                return self.x + self.indent[0] * (2 * n + 1) + n * btn_w
        else:
            raise ValueError
        lbl_w = btn_w
        lbl_h = btn_h

        self.lbl_x = btn_x
        self.lbl_y = btn_y
        self.btn_w = btn_w
        self.btn_h = btn_h
        self.btn_x = btn_x
        self.btn_y = btn_y

        ll = self.mll.get_list()
        lb = self.mbl.get_list()
        cl = 0
        cb = 0
        for ind in range(len(lb) + len(ll)):
            if self.place[ind] == 'b':
                btn = lb[cb]
                btn.x = self.btn_x(ind)
                btn.y = self.btn_y(ind)
                btn.w = btn_w
                btn.h = btn_h
                cb += 1
            elif self.place[ind] == 'l':
                lbl = ll[cl]
                lbl.x = self.lbl_x(ind)
                lbl.y = self.lbl_y(ind)
                lbl.w = lbl_w
                lbl.h = lbl_h
                lbl.calculation()
                cl += 1
            else:
                raise ValueError

    def show(self, screen) -> None:
        """
        Метод для отрисовки слоя и содержимого

        :param screen: Холст
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
        self.mbl.show(screen)
        self.mll.show(screen)
