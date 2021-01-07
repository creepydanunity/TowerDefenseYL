import pygame.draw

from main_game import start


def start_game():
    start()


class MenuButton(object):

    def __init__(self, x, y, w, h, func=lambda x: x, color="#ffffff", weight=0) -> None:
        """
        Инициализация кнопки
        :param x: Координата x
        :param y: Координата y
        :param w: Ширина
        :param h: Высота
        :param func: Функция, которую выполняет кнопка при нажатии
        :param color: Цвет кнопки
        :param weight: Ширина рамки при отрисовке
        """
        if x < 0 or y < 0 or w < 0 or h < 0:
            raise ValueError
        if type(x) != int or type(y) != int or type(w) != int or type(h) != int or type(color) != str:
            raise TypeError
        if type(func) != type(lambda x: x):
            raise TypeError
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func
        self.color = color
        self.weight = weight

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
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), self.weight)


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
        :param pos: Позиция курсора
        :return: Возвращает список нажатых
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
