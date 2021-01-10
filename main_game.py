from random import randint

import pygame

from menu_exemplars import layout, layout2, btn
from settings import get_resolution
from random import randint
import copy


class Board:
    """
    :type Классическое клеточное игровое поле для TDшки.
    """

    def __init__(self, width, height):
        """
        :param width: Ширина поля в клетках
        :param height: Высота поля в клетках
        """
        self.board = [[1] * width for _ in range(height)]
        self.width, self.height = width, height
        self.left, self.top, self.cell_size = None, None, None
        self.size = width * height
        self.generate_way()

    def generate_way(self, road_forks=1):
        """
        :param road_forks: Кол-во развилок. Высчитывается по известной лишь мне формуле.
        :return: Занимается генерацией карты - self.board, ничего конкретного не возвращает.
        """
        path_length = self.width * self.height // 5

        def new_way():
            # Сначала расставляет рейтинг клеток для создания развилки.
            # Потом создаёт её на основе полученного рейтинга.
            Rate_book = {}
            point_coord = (0, 0)
            for column in range(3, len(self.board) - 3):
                for row in range(3, len(self.board[column]) - 2):
                    if self.board[column][row] == 5 or \
                            self.board[column - 1][row] == 5 or \
                            self.board[column + 1][row] == 5 or \
                            self.board[column][row + 1] == 5 or \
                            self.board[column][row - 1] == 5 or \
                            self.board[column - 1][row - 1] == 5 or \
                            self.board[column - 1][row + 1] == 5 or \
                            self.board[column + 1][row + 1] == 5 or \
                            self.board[column + 1][row - 1] == 5:
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
                        cell_in_line_counter = 0
                        for ii in self.board[row]:
                            if ii == 5:
                                cell_in_line_counter += 1
                        for ii in range(len(self.board)):
                            if self.board[ii][column] == 5:
                                cell_in_line_counter += 1
                        median = ((len(self.board)) // 2, len(self.board[0]) // 2)
                        gip = (abs(median[0] - row) ** 2 + abs(median[1] - column) ** 2) ** 0.5
                        if gip == 0:
                            if near is False:
                                Rate_book[(row, column)] = ((cell_in_line_counter / self.size), near)
                        else:
                            Rate_book[(row, column)] = ((cell_in_line_counter / self.size) * gip, near)

            if len(Rate_book.keys()) / (self.width * self.height) > 0.1 or len(Rate_book.keys()) == 0:
                print('No')
                self.generate_way()
            else:
                temp_max_value = sorted(Rate_book.values(), reverse=True)[0]
                for key, value in Rate_book.items():
                    if value == temp_max_value:
                        point_coord = key
                        break
                # self.board[point_coord[1]][point_coord[0]] = 22
                minimum_distances = []
                for row in range(0, len(self.board)):
                    for column in range(3, point_coord[0] + 1):
                        near_cell_way_counter = 0
                        if self.board[row][column] == 5:
                            to_right = False
                            if self.board[row - 1][column] == 5 and self.board[row + 1][column] != 5:
                                near_cell_way_counter += 1
                            elif self.board[row + 1][column] == 5 and self.board[row - 1][column] != 5:
                                near_cell_way_counter += 1
                            if self.board[row][column + 1] == 5 and self.board[row][column - 1] != 5:
                                near_cell_way_counter += 1
                                to_right = True
                            elif self.board[row][column - 1] == 5 and self.board[row][column + 1] != 5:
                                near_cell_way_counter += 1
                                to_right = True
                            if near_cell_way_counter >= 2:
                                # self.board[row][column] = 22
                                go_up, go_down, go_left, go_right = False, False, False, False
                                if to_right and self.board[row + 1][column] == 5:
                                    if row < point_coord[1]:
                                        continue
                                    else:
                                        go_up = True
                                elif to_right and self.board[row - 1][column] == 5:
                                    if row > point_coord[1]:
                                        continue
                                    else:
                                        go_down = True
                                elif self.board[row][column - 1] == 5:
                                    go_right = True
                                else:
                                    go_right = True
                                gip = (abs(point_coord[0] - column) ** 2 + abs(point_coord[1] - row) ** 2) ** 0.5
                                if go_right:
                                    minimum_distances.append([gip, [row, column], 'go_right'])
                                elif go_down:
                                    minimum_distances.append([gip, [row, column], 'go_down'])
                                elif go_up:
                                    minimum_distances.append([gip, [row, column], 'go_up'])
                if minimum_distances:
                    final_start_fork = []
                    minimum_distances = sorted(minimum_distances, key=lambda x: x[0], reverse=True)
                    print(minimum_distances)
                    for minimum_distance in minimum_distances:
                        passed_fork = True
                        temp_distance = copy.deepcopy(minimum_distance)
                        point_coord = (point_coord[1], point_coord[0])
                        if minimum_distance[2] == 'go_right':
                            while point_coord[1] > minimum_distance[1][1]:
                                minimum_distance[1][1] += 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[0] > minimum_distance[1][0]:
                                    minimum_distance[1][0] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            passed_fork = False
                                            break
                                while point_coord[0] < minimum_distance[1][0]:
                                    minimum_distance[1][0] -= 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        elif minimum_distance[2] == 'go_down':
                            while point_coord[0] > minimum_distance[1][0]:
                                minimum_distance[1][0] += 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        elif minimum_distance[2] == 'go_up':
                            while point_coord[0] < minimum_distance[1][0]:
                                minimum_distance[1][0] -= 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        if passed_fork:
                            final_start_fork = temp_distance
                            print(final_start_fork)
                            break
                    if final_start_fork:
                        # self.board[final_start_fork[1][0]][final_start_fork[1][1]] = 22
                        minimum_distance = final_start_fork
                        if minimum_distance[2] == 'go_right':
                            while point_coord[1] > minimum_distance[1][1]:
                                minimum_distance[1][1] += 1
                                self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                            if minimum_distance != point_coord:
                                while point_coord[0] > minimum_distance[1][0]:
                                    minimum_distance[1][0] += 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                while point_coord[0] < minimum_distance[1][0]:
                                    minimum_distance[1][0] -= 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                        elif minimum_distance[2] == 'go_down':
                            while point_coord[0] > minimum_distance[1][0]:
                                minimum_distance[1][0] += 1
                                self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                            if minimum_distance != point_coord:
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                        elif minimum_distance[2] == 'go_up':
                            while point_coord[0] < minimum_distance[1][0]:
                                minimum_distance[1][0] -= 1
                                self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                            while point_coord[1] < minimum_distance[1][1]:
                                minimum_distance[1][1] -= 1
                                self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                        temp, cell_found = minimum_distance[1][1] + 1, False
                        while temp < self.width - 1:
                            self.board[minimum_distance[1][0]][temp] = 5
                            temp += 1
                            if self.board[minimum_distance[1][0]][temp] == 5 or \
                                    self.board[minimum_distance[1][0] - 1][temp] == 5 or \
                                    self.board[minimum_distance[1][0] + 1][temp] == 5:
                                cell_found = True
                                break
                        if not cell_found:
                            if minimum_distance[1][0] > finish_pos[0]:
                                while minimum_distance[1][0] != finish_pos[0]:
                                    minimum_distance[1][0] -= 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                            else:
                                while minimum_distance[1][0] != finish_pos[0]:
                                    minimum_distance[1][0] += 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                    else:
                        print('Re-generate')
                        self.generate_way()
                else:
                    print('Re-generate')
                    self.generate_way()
        while True:
            fork, swap_direction, cells, direction_x, direction_y, space = 0, 0, 0, 1, 0, 0
            self.board = [[1] * self.width for _ in range(self.height)]
            y = randint(3, self.height - 2)
            self.board[y][1] = 9
            current_pos = (y, 1)
            y = randint(2, self.height - 1)
            self.board[y][self.width - 2] = 8
            finish_pos = (y, self.width - 2)
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
            if path_length - 5 <= cells * 1.15:
                self.board[finish_pos[0]][finish_pos[1]] = 8
                for j in range(road_forks):
                    new_way()
                break
        # for i in self.board:
            # print(i)

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
                elif self.board[i][j] == 99:
                    pygame.draw.rect(screen,
                                     (7, 204, 147),
                                     (j * self.cell_size[0] + self.left,
                                      i * self.cell_size[1] + self.top,
                                      self.cell_size[0], self.cell_size[1]), self.board[i][j], 0)
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

    while running:
        board_clear(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                btn.get_clicked(event.pos)

        board_update(game_map, screen)

        layout.show(screen)
        layout2.show(screen)

    pygame.quit()


def board_update(game_map, screen):
    game_map.render(screen)


def board_clear(screen):
    pygame.display.flip()
    screen.fill((0, 0, 0))
