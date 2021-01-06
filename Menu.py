import pygame.draw

from main_game import start


def start_game():
    start()


class MenuButton(object):

    def __init__(self, x, y, w, h, func=lambda x: x):
        if x < 0 or y < 0 or w < 0 or h < 0:
            raise ValueError
        if type(x) != int or type(y) != int or type(w) != int or type(h) != int:
            raise TypeError
        if type(func) != type(lambda x: x):
            raise TypeError
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func

    def is_clicked(self, pos: tuple) -> bool:
        x1, y1 = pos
        if self.x <= x1 <= self.x + self.w:
            if self.y <= y1 <= self.y + self.h:
                return True
        return False

    def on_click(self):
        eval('self.func()')

    def get_clicked(self, pos):
        if self.is_clicked(pos):
            self.on_click()

    def show(self, screen, color='#ffffff', weight=0):
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), weight)
