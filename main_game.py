import pygame
from settings import get_resolution


class Board:
    def __init__(self, x, y, w=50):
        self.x, self.y, self.w = x, y, w
        self.board = [[0] * x for _ in range(y)]
        self.left, self.top = 100, 100


def start():
    temporary_xy = list(map(int, input("Кол-во клеток, x; y").split()))
    game_map = Board(temporary_xy[0], temporary_xy[1])
    pygame.init()
    screen = pygame.display.set_mode(get_resolution(), flags=pygame.FULLSCREEN)
    running = True
    while running:
        board_update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


def board_update():
    pygame.display.flip()
