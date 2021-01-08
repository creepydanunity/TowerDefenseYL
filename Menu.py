import pygame.draw
import pygame.font


# from main_game import start


# def start_game():
#     start()


class MenuButton(object):

    def __init__(self, x: int, y: int, w: int, h: int, func=lambda: None, color="#ffffff", weight=0, text="",
                 text_color="#000000", text_size=50) -> None:
        """
        Инициализация кнопки

        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param func: Функция, которую выполняет кнопка при нажатии
        :param color: Цвет кнопки
        :param weight: Ширина рамки при отрисовке
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
        self.weight = weight
        self.text = text
        self.text_color = text_color
        self.text_size = text_size

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
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), self.weight)
        screen.blit(text, (text_x, text_y))


class MenuList(list):

    def __init__(self, li=None) -> None:
        """
        Инициализация списка всех кнопок

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
