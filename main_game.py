from random import randint

import pygame

from Menu import MenuButton, MenuList, MenuLayOut
from settings import get_resolution


class Board:
    def __init__(self, width, height):
        self.board = [[1] * width for _ in range(height)]
        self.width, self.height = width, height
        self.left, self.top, self.cell_size = None, None, None
        self.generate_way()

    def generate_way(self, road_forks=1, base=1, spawn=1):
        path_length = self.width * self.height // 5

        def new_way(end_pos):
            raiting_book = {}
            for row in range(3, len(self.board) - 3):
                for column in range(3, len(self.board[row]) - 2):
                    if self.board[column][row] == 5:
                        continue
                    elif self.board[column - 1][row] == 5:
                        continue
                    elif self.board[column + 1][row] == 5:
                        continue
                    elif self.board[column][row + 1] == 5:
                        continue
                    elif self.board[column][row - 1] == 5:
                        continue
                    elif self.board[column - 1][row - 1] == 5:
                        continue
                    elif self.board[column - 1][row + 1] == 5:
                        continue
                    elif self.board[column + 1][row + 1] == 5:
                        continue
                    elif self.board[column + 1][row - 1] == 5:
                        continue
                    else:
                        if self.board[column][row + 2] == 5 or \
                                self.board[column][row - 2] == 5 or \
                                self.board[column - 1][row - 2] == 5 or \
                                self.board[column - 1][row + 2] == 5 or \
                                self.board[column + 1][row - 2] == 5 or \
                                self.board[column + 1][row - 2] == 5 or \
                                self.board[column + 2][row + 1] == 5 or \
                                self.board[column + 2][row - 1] == 5 or \
                                self.board[column + 2][row + 2] == 5 or \
                                self.board[column + 2][row - 2] == 5 or \
                                self.board[column + 2][row] == 5 or \
                                self.board[column - 2][row] == 5 or \
                                self.board[column - 2][row + 1] == 5 or \
                                self.board[column - 2][row - 1] == 5 or \
                                self.board[column - 2][row + 2] == 5 or \
                                self.board[column - 2][row - 2] == 5:
                            continue
                        else:
                            near = False
                        rait_counter = 0
                        cells = 0
                        for i in self.board[row]:
                            if i == 5:
                                rait_counter += 1
                            cells += 1
                        for i in range(len(self.board)):
                            if self.board[column][i] == 5:
                                rait_counter += 1
                            cells += 1
                        mediana = ((len(self.board)) // 2, len(self.board[0]) // 2)
                        gip = (abs(mediana[0] - row) ** 2 + abs(mediana[1] - column) ** 2) ** 0.5
                        if gip == 0:
                            if near is False:
                                raiting_book[(row, column)] = ((rait_counter / cells), near)
                        else:
                            raiting_book[(row, column)] = ((rait_counter / cells) / gip, near)
            if len(raiting_book.keys()) / (self.width * self.height) > 0.1:
                print('No')
                self.generate_way()
            else:
                for i in raiting_book.keys():
                    row, col = i[0], i[1]
                    if raiting_book[i][1] is False:
                        self.board[col][row] = 3
                    else:
                        self.board[col][row] = 2

        while True:
            fork, swap_direction, cells = 0, 0, 0
            self.board = [[1] * self.width for _ in range(self.height)]
            y = randint(3, self.height - 2)
            self.board[y][1] = 9
            current_pos = (y, 1)
            y = randint(2, self.height - 1)
            self.board[y][self.width - 2] = 8
            finish_pos = (y, self.width - 2)
            direction_x = 1
            direction_y = 0
            space = 0

            while current_pos != finish_pos:
                if space == 0:
                    if swap_direction > 1:
                        if direction_x == 0:
                            temp_random = randint(1, 7)
                            if temp_random in range(1, 4):
                                direction_y = 0
                                direction_x = 1
                                space = 2
                        else:
                            temp_random = randint(1, 2)
                            direction_x = 0
                            if temp_random == 1:
                                direction_y = 1
                            else:
                                direction_y = -1
                        swap_direction = 0
                    else:
                        swap_direction += 1
                else:
                    space -= 1
                    swap_direction += 1

                if current_pos[0] + direction_y < 1:
                    direction_y = 0
                    direction_x = 1
                elif current_pos[0] + direction_y >= self.height - 1:
                    direction_y = 0
                    direction_x = 1

                if current_pos[1] + direction_x >= self.width:
                    direction_x = 0
                    if current_pos[0] > finish_pos[0]:
                        direction_y = -1
                    elif current_pos[0] < finish_pos[0]:
                        direction_y = 1
                    else:
                        cells += 1

                if current_pos[0] == 1:
                    if self.board[current_pos[0] + 1][current_pos[1] - 1] == 5:
                        direction_y = 0
                        direction_x = 1
                elif current_pos[0] == self.height - 2:
                    if self.board[current_pos[0] - 1][current_pos[1] - 1] == 5:
                        direction_y = 0
                        direction_x = 1
                if current_pos != finish_pos:
                    if current_pos[1] + 1 == finish_pos[1]:
                        direction_y = 0
                        direction_x = 1
                    elif current_pos[1] == finish_pos[1]:
                        direction_x = 0
                        if current_pos[0] > finish_pos[0]:
                            direction_y = -1
                        elif current_pos[0] < finish_pos[0]:
                            direction_y = 1
                    current_pos = (current_pos[0] + direction_y, current_pos[1] + direction_x)
                    cells += 1
                    self.board[current_pos[0]][current_pos[1]] = 5
                else:
                    break
            if path_length - 7 <= cells <= path_length + 7:
                self.board[finish_pos[0]][finish_pos[1]] = 8
                for j in range(road_forks):
                    new_way(end_pos=finish_pos)
                break
        for i in self.board:
            print(i)

    def set_view(self, w2, h2):
        w, h = get_resolution()
        self.left, self.top = w // 12, h // 12
        self.cell_size = ((w - w // 12) // w2, (h - h // 12) // h2)

    def get_cell(self, mouse_pos):
        mouse_pos = mouse_pos[0] - self.left, mouse_pos[1] - self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.cell_size[0] * j < mouse_pos[0] < self.cell_size[0] * (j + 1):
                    if self.cell_size[1] * i < mouse_pos[1] < self.cell_size[1] * (i + 1):
                        return j, i
        return None

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 9:
                    pygame.draw.rect(screen,
                                     (255, 0, 0),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 50)
                elif self.board[i][j] == 8:
                    pygame.draw.rect(screen,
                                     (0, 255, 0),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 50)
                elif self.board[i][j] == 5:
                    pygame.draw.rect(screen,
                                     (255, 255, 0),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 0)
                elif self.board[i][j] == 3:
                    pygame.draw.rect(screen,
                                     (255, 0, 190),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 0)
                else:
                    pygame.draw.rect(screen,
                                     (255, 255, 255),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 0)

    def get_click(self, event_pos):
        tmp = self.get_cell(event_pos)
        if tmp:
            self.on_click(tmp)
        print(tmp)

    def on_click(self, cell):
        if self.board[cell[1]][cell[0]] == 0:
            self.board[cell[1]][cell[0]] = 1
        else:
            self.board[cell[1]][cell[0]] = 0


def start():
    temporary_xy = list(map(int, input("Кол-во клеток, x; y\n").split()))
    game_map = Board(temporary_xy[0], temporary_xy[1])
    game_map.set_view(temporary_xy[0], temporary_xy[1])
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    running = True

    def print_1():
        print(1)

    def print_2():
        print(2)

    def print_3():
        print(3)

    def print_4():
        print(4)

    s = 15
    btn1 = MenuButton(0, 0, 0, 0, func=print_1, color="#737373", text="Начать", text_color="#1a1a1a", text_size=s)
    btn2 = MenuButton(0, 0, 0, 0, func=print_2, color="#737373", text="Заново", text_color="#1a1a1a", text_size=s)
    btn3 = MenuButton(0, 0, 0, 0, func=print_3, color="#737373", text="Настройки", text_color="#1a1a1a", text_size=s)
    btn4 = MenuButton(0, 0, 0, 0, func=print_4, color="#737373", text="Выйти", text_color="#1a1a1a", text_size=s)
    btn5 = f'MenuButton(0, 0, 0, 0, func=print_4, color="#737373", text="*кнопка*", text_color="#1a1a1a", text_size={s})'
    li = []
    for x in range(1, 5):
        eval(f'li.append(btn{x})')
    for x in range(5):
        li.append(eval(btn5))
    btn = MenuList(li)
    layout = MenuLayOut(btn, 0, 0, 60, 600, (5, 5), "#cccccc", 'v')

    while running:
        board_clear(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                btn.get_clicked(event.pos)

        board_update(game_map, screen)

        layout.show(screen)

    pygame.quit()


def board_update(game_map, screen):
    game_map.render(screen)


def board_clear(screen):
    pygame.display.flip()
    screen.fill((0, 0, 0))
